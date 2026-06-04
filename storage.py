"""Shared JSON-file persistence for CaféLibro."""
import json
from pathlib import Path

DEFAULT_DATA_PATH = Path("data/library.json")
EMPTY_STATE = {"members": [], "books": [], "loans": []}


def load_state(path: Path = DEFAULT_DATA_PATH) -> dict:
    """Read state from disk; return an empty state if the file is missing."""
    if not path.exists():
        return {k: list(v) for k, v in EMPTY_STATE.items()}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict, path: Path = DEFAULT_DATA_PATH) -> None:
    """Write state to disk, creating the parent directory if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)