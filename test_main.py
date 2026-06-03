import pytest
import os
import main

# Cambiado para que coincida con la nueva convención
TEST_DATA_FILE = "test_store.json"

@pytest.fixture(autouse=True)
def setup_and_teardown(monkeypatch):
    """Fija el archivo de datos a uno de prueba temporal antes de cada test."""
    monkeypatch.setattr(main, "DATA_FILE", TEST_DATA_FILE)
    
    # Asegurar un estado limpio antes de la prueba
    if os.path.exists(TEST_DATA_FILE):
        os.remove(TEST_DATA_FILE)
        
    yield 
    
    # Limpiar el archivo de prueba después
    if os.path.exists(TEST_DATA_FILE):
        os.remove(TEST_DATA_FILE)

def test_register_book_success():
    """Prueba el registro exitoso de un libro."""
    main.register_book("Fundación", "SCI-001")
    
    data = main.load_data()
    assert "SCI-001" in data["books"]
    assert data["books"]["SCI-001"]["title"] == "Fundación"
    assert data["books"]["SCI-001"]["status"] == "available"

def test_register_book_duplicate_code():
    """Prueba que un código duplicado lanza una excepción."""
    main.register_book("Dune", "SCI-002")
    
    with pytest.raises(ValueError) as excinfo:
        main.register_book("El Mesías de Dune", "SCI-002")
        
    assert "ya existe en el catálogo" in str(excinfo.value)