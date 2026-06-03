import json
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


if __name__ == "__main__":
    cmd_overdue()

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
