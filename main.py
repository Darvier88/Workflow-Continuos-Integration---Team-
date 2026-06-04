"""Gestor de prestamos de biblioteca.

Estado en memoria y operaciones basicas. Solo libreria estandar.
"""

BASE_STATE_FILE = os.path.join(os.path.dirname(__file__), "base.json")


def empty_state():
    """Devuelve una estructura de estado nueva y vacia."""
    return {"members": [], "books": [], "loans": []}


def load_base_state(path=BASE_STATE_FILE):
    """Carga el estado base desde un archivo JSON.

    Si el archivo no existe, devuelve un estado vacio nuevo.
    """
    if not os.path.exists(path):
        return empty_state()
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def register_member(state, member_id, name):
    """Registra un miembro nuevo en el estado.

    Valida que member_id y name no esten vacios ni en blanco y que el
    member_id no exista ya. Devuelve el diccionario del miembro registrado.
    """
    if member_id is None or not str(member_id).strip():
        raise ValueError("Member identifier cannot be empty")
    if name is None or not str(name).strip():
        raise ValueError("Member name cannot be empty")

    for member in state["members"]:
        if member["member_id"] == member_id:
            raise ValueError(
                "Member identifier already exists: {}".format(member_id)
            )

    member = {"member_id": member_id, "name": name}
    state["members"].append(member)
    return member
import json
import os
import argparse

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
    with open(filepath, 'r') as file:
        data = json.load(file)
    if book_id in data.get("active_loans", {}):
        del data["active_loans"][book_id]
        for book in data.get("books", []):
            if book["id"] == book_id:
                book["available"] = True
                break
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    else:
        raise ValueError("El libro no está prestado actualmente.")

def list_member_loans(member_id: str, db_path: str = "store.json") -> str:
    """Lista los préstamos activos de un miembro."""
    if not os.path.exists(db_path):
        return f"Error: No se encontró el archivo de base de datos '{db_path}'."
    with open(db_path, 'r', encoding='utf-8') as file:
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

def main():
    parser = argparse.ArgumentParser(description="CaféLibro - Gestión de Préstamos")
    subparsers = parser.add_subparsers(dest="command")

    # Subcomando: add-book
    add_parser = subparsers.add_parser("add-book", help="Registrar un nuevo libro")
    add_parser.add_argument("title", type=str)
    add_parser.add_argument("code", type=str)

    # Subcomando: list-loans
    list_parser = subparsers.add_parser("list-loans", help="Ver préstamos de un miembro")
    list_parser.add_argument("member_id", type=str)

    args = parser.parse_args()

    if args.command == "add-book":
        try:
            print(register_book(args.title, args.code))
        except ValueError as e:
            print(e)
    elif args.command == "list-loans":
        print(list_member_loans(args.member_id))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
