import json
import pytest
from main import list_member_loans

@pytest.fixture
def temp_store(tmp_path):
    db_data = {
        "books": [
            {"code": "B001", "title": "Project Hail Mary"},
            {"code": "B002", "title": "Fundamentos de Programación en Python"}
        ],
        "members": [
            {"id": "M001", "name": "Jorge Bravo"},
            {"id": "M002", "name": "Usuario Sin Préstamos"}
        ],
        "loans": [
            {"book_code": "B001", "member_id": "M001", "due_date": "2026-06-10"},
            {"book_code": "B002", "member_id": "M001", "due_date": "2026-06-15"}
        ]
    }
    
    file_path = tmp_path / "store.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(db_data, f)
        
    return str(file_path)

def test_list_member_loans_with_books(temp_store):
    result = list_member_loans("M001", db_path=temp_store)
    
    assert "Project Hail Mary" in result
    assert "B001" in result
    assert "Fundamentos de Programación en Python" in result
    assert "B002" in result

def test_list_member_loans_no_books(temp_store):
    result = list_member_loans("M002", db_path=temp_store)
    
    assert "no tiene libros en préstamo actualmente" in result

def test_list_member_loans_invalid_member(temp_store):
    result = list_member_loans("M999", db_path=temp_store)
    
    assert "no está registrado en el sistema" in result

def test_missing_db_file():
    result = list_member_loans("M001", db_path="archivo_inexistente.json")
    
    assert "Error: No se encontró el archivo de base de datos" in result