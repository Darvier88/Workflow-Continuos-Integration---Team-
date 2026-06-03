"""Gestor de prestamos de biblioteca.

Estado en memoria y operaciones basicas. Solo libreria estandar.
"""

import json
import os

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
