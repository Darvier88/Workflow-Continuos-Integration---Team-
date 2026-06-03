import json
import os
import argparse

DATA_FILE = "store.json"

def load_data():
    """Carga los datos del archivo JSON. Si no existe, devuelve la estructura inicial."""
    if not os.path.exists(DATA_FILE):
        return {"books": {}, "members": {}, "loans": {}}
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Guarda los datos en el archivo JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def register_book(title: str, book_code: str):
    """
    Registra un libro en el catálogo con un título y un código único.
    """
    data = load_data()
    
    if book_code in data["books"]:
        raise ValueError(f"Error: El libro con el código '{book_code}' ya existe en el catálogo.")
    
    data["books"][book_code] = {
        "title": title,
        "status": "available"
    }
    
    save_data(data)
    return f"Éxito: Libro '{title}' (Código: {book_code}) registrado."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CaféLibro Gestor de Préstamos")
    parser.add_argument("--add-book", nargs=2, metavar=("TITULO", "CODIGO"), help="Registrar un nuevo libro")
    
    args = parser.parse_args()
    
    if args.add_book:
        title, code = args.add_book
        try:
            resultado = register_book(title, code)
            print(resultado)
        except ValueError as e:
            print(e)