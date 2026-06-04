import json
import os
import pytest
from main import return_book

TEST_FILE = "test_data.json"


def setup_function():
    """Prepara un archivo JSON de prueba antes de cada test."""
    test_data = {
        "books": [
            {
                "id": "B01",
                "title": "Estructuras de Backend",
                "available": False
            }
        ],
        # El libro B01 está prestado al miembro M01
        "active_loans": {"B01": "M01"}
    }
    with open(TEST_FILE, 'w') as f:
        json.dump(test_data, f)


def teardown_function():
    """Limpia el archivo de prueba después de cada test."""
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_return_book_success():
    """Prueba que un libro prestado se devuelve correctamente."""
    result = return_book("B01", filepath=TEST_FILE)
    assert result is True

    # Verificar que el JSON se actualizó correctamente
    with open(TEST_FILE, 'r') as f:
        data = json.load(f)

    # El libro ya no debe estar en préstamos activos
    assert "B01" not in data["active_loans"]
    assert data["books"][0]["available"] is True


def test_return_book_not_loaned():
    """Prueba error si se intenta devolver un libro no prestado."""
    error_msg = "El libro no está prestado actualmente."
    with pytest.raises(ValueError, match=error_msg):
        return_book("B99", filepath=TEST_FILE)