import json
import os
import argparse
from datetime import date
from overdue import report_overdue


def cmd_overdue():
    with open("data.json", encoding="utf-8") as f:
        state = json.load(f)
    vencidos = report_overdue(state["loans"], date.today().isoformat())
    if not vencidos:
        print("No hay préstamos vencidos.")
    for ln in vencidos:
        print(f"Libro {ln['book_code']} — miembro {ln['member_id']} — vencía {ln['due_date']}")

def return_book(book_id, filepath="library_data.json"):
    """
    Devuelve un libro y lo marca como disponible en el archivo JSON.
    """
    # Cargar los datos actuales
    with open(filepath, 'r') as file:
        data = json.load(file)

    # Verificar si el libro está en los préstamos activos
    if book_id in data.get("active_loans", {}):
        # Eliminar de préstamos activos
        del data["active_loans"][book_id]

        # Marcar el libro como disponible en el catálogo
        for book in data.get("books", []):
            if book["id"] == book_id:
                book["available"] = True
                break

        # Guardar los cambios en el JSON
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    else:
        # Reportar un error claro si el libro no está prestado
        raise ValueError("El libro no está prestado actualmente.")


def list_member_loans(member_id: str, db_path: str = "store.json") -> str:
    
    if not os.path.exists(db_path):
        return f"Error: No se encontró el archivo de base de datos '{db_path}'."

    with open(db_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return f"Error: El archivo '{db_path}' está corrupto o no es un JSON válido."

    members = data.get("members", [])
    if not any(m.get("id") == member_id for m in members):
        return f"Error: El miembro con ID '{member_id}' no está registrado en el sistema."

    active_loans = [loan for loan in data.get("loans", []) if loan.get("member_id") == member_id]

    if not active_loans:
        return f"El miembro '{member_id}' no tiene libros en préstamo actualmente."

    books = data.get("books", [])
    result_lines = [f"Libros actualmente en préstamo para el miembro '{member_id}':"]
    
    for loan in active_loans:
        book_code = loan.get("book_code")
        book = next((b for b in books if b.get("code") == book_code), None)
        
        if book:
            result_lines.append(f"- {book.get('title')} (Código: {book_code})")
        else:
            result_lines.append(f"- [Libro no encontrado en el catálogo] (Código: {book_code})")

    return "\n".join(result_lines)


def main():
    parser = argparse.ArgumentParser(
        description="CaféLibro - Sistema de Gestión de Préstamos",
        epilog="Ejecuta 'python main.py <comando> -h' para más detalles de cada comando."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    list_parser = subparsers.add_parser(
        "list-loans", 
        help="Muestra los libros que un miembro tiene actualmente en préstamo."
    )
    list_parser.add_argument(
        "member_id", 
        type=str, 
        help="El ID único del miembro (ej. M001)"
    )
    subparsers.add_parser(
        "overdue",
        help="Reporta los préstamos vencidos."
    )

    args = parser.parse_args()

    if args.command == "list-loans":
        resultado = list_member_loans(args.member_id)
        print(resultado)
    elif args.command == "overdue":
        cmd_overdue()
        
    elif args.command is None:
        parser.print_help()
    else:
        print("Error: Comando no reconocido o aún no implementado.")

if __name__ == "__main__":
    main()
