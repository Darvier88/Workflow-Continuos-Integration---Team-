"""CaféLibro CLI entry point and legacy feature helpers."""
import argparse
import json
import os
import sys

import loans

DATA_FILE = "store.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"books": {}, "members": {}, "loans": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def register_book(title: str, book_code: str):
    """Registra un libro en el catálogo."""
    data = load_data()
    if book_code in data["books"]:
        raise ValueError(f"Error: El libro con código '{book_code}' ya existe en el catálogo.")
    data["books"][book_code] = {"title": title, "status": "available"}
    save_data(data)
    return f"Éxito: Libro '{title}' (Código: {book_code}) registrado."


def return_book(book_id, filepath="library_data.json"):
    """Devuelve un libro y lo marca como disponible."""
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    if book_id in data.get("active_loans", {}):
        del data["active_loans"][book_id]
        for book in data.get("books", []):
            if book["id"] == book_id:
                book["available"] = True
                break
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    raise ValueError("El libro no está prestado actualmente.")


def list_member_loans(member_id: str, db_path: str = "store.json") -> str:
    """Lista los préstamos activos de un miembro."""
    if not os.path.exists(db_path):
        return f"Error: No se encontró el archivo de base de datos '{db_path}'."
    with open(db_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return f"Error: El archivo '{db_path}' está corrupto."
    members = data.get("members", [])
    if not any(m.get("id") == member_id for m in members):
        return f"Error: El miembro '{member_id}' no está registrado en el sistema."
    active_loans = [l for l in data.get("loans", []) if l.get("member_id") == member_id]
    if not active_loans:
        return f"El miembro '{member_id}' no tiene libros en préstamo actualmente."
    books = data.get("books", [])
    lines = [f"Préstamos activos para '{member_id}':"]
    for loan in active_loans:
        code = loan.get("book_code")
        book = next((b for b in books if b.get("code") == code), None)
        lines.append(f"- {book.get('title') if book else '[No encontrado]'} (Código: {code})")
    return "\n".join(lines)


def _cli_add_book(args) -> int:
    try:
        print(register_book(args.title, args.code))
    except ValueError as e:
        print(e)
        return 1
    return 0


def _cli_list_loans(args) -> int:
    print(list_member_loans(args.member_id))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cafelibro", description="CaféLibro - Gestión de Préstamos")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add-book", help="Registrar un nuevo libro")
    add_parser.add_argument("title", type=str)
    add_parser.add_argument("code", type=str)
    add_parser.set_defaults(func=_cli_add_book)

    list_parser = subparsers.add_parser("list-loans", help="Ver préstamos de un miembro")
    list_parser.add_argument("member_id", type=str)
    list_parser.set_defaults(func=_cli_list_loans)

    loans.register_parser(subparsers)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
