"""History management for GeneWeaver."""

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.config import OUTPUT_DIR


HISTORY_FILE = OUTPUT_DIR / "analysis_history.json"
_history_lock = threading.Lock()


def _load_history() -> list:
    """Load saved history from JSON file."""

    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def _save_history(history: list) -> None:
    """Save history safely to JSON file."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    temporary_file = HISTORY_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)

    temporary_file.replace(HISTORY_FILE)


def add_history_entry(
    operation: str,
    input_data,
    result,
) -> dict:
    """Add a new analysis or alignment record."""

    entry = {
        "id": str(uuid4()),
        "operation": operation,
        "input": input_data,
        "result": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    with _history_lock:
        history = _load_history()
        history.append(entry)
        _save_history(history)

    return entry


def get_history(limit: int | None = None) -> list:
    """Return saved history, newest first."""

    with _history_lock:
        history = _load_history()

    history.reverse()

    if limit is not None:
        if limit < 0:
            raise ValueError("Limit cannot be negative.")
        history = history[:limit]

    return history


def get_history_entry(entry_id: str) -> dict | None:
    """Find a history record by its ID."""

    with _history_lock:
        history = _load_history()

    for entry in history:
        if entry.get("id") == entry_id:
            return entry

    return None


def delete_history_entry(entry_id: str) -> bool:
    """Delete one history record."""

    with _history_lock:
        history = _load_history()
        updated_history = [
            entry for entry in history
            if entry.get("id") != entry_id
        ]

        if len(updated_history) == len(history):
            return False

        _save_history(updated_history)

    return True


def clear_history() -> int:
    """Delete all history records and return deleted count."""

    with _history_lock:
        history = _load_history()
        deleted_count = len(history)
        _save_history([])

    return deleted_count


def get_history_count() -> int:
    """Return the number of saved records."""

    with _history_lock:
        return len(_load_history())


__all__ = [
    "add_history_entry",
    "get_history",
    "get_history_entry",
    "delete_history_entry",
    "clear_history",
    "get_history_count",
]
