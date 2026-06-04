"""Pruebas para la feature de registro de miembros."""

import os
import sys

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from main import empty_state, register_member  # noqa: E402


def test_registro_exitoso():
    state = empty_state()

    registered = register_member(state, "M-001", "Luis Cedeno")

    assert registered == {"member_id": "M-001", "name": "Luis Cedeno"}
    assert len(state["members"]) == 1
    assert state["members"][0]["member_id"] == "M-001"
    assert state["members"][0]["name"] == "Luis Cedeno"


def test_id_duplicado():
    state = empty_state()
    register_member(state, "M-001", "Luis Cedeno")

    with pytest.raises(ValueError):
        register_member(state, "M-001", "Otro Nombre")

    assert len(state["members"]) == 1


def test_campos_vacios():
    state = empty_state()

    with pytest.raises(ValueError):
        register_member(state, "", "Luis Cedeno")

    with pytest.raises(ValueError):
        register_member(state, "M-002", "   ")

    assert len(state["members"]) == 0
