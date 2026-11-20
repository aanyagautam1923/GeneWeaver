"""SQLite database manager for GeneWeaver."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.config import PROJECT_ROOT


DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "geneweaver.db"


def get_connection():
    """Create and return a SQLite database connection."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create database tables if they do not exist."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                input_data TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_record(
    operation: str,
    input_data,
    result,
) -> int:
    """Save an analysis or alignment record."""

    if not operation:
        raise ValueError("Operation cannot be empty.")

    input_json = json.dumps(input_data, ensure_ascii=False)
    result_json = json.dumps(result, ensure_ascii=False)

    created_at = datetime.now(timezone.utc).isoformat()

    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO analysis_history
            (operation, input_data, result, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (operation, input_json, result_json, created_at),
        )

        return cursor.lastrowid


def get_records(limit: int | None = None) -> list:
    """Retrieve saved records, newest first."""

    if limit is not None and limit < 0:
        raise ValueError("Limit cannot be negative.")

    initialize_database()

    query = """
        SELECT * FROM analysis_history
        ORDER BY id DESC
    """

    if limit is not None:
        query += " LIMIT ?"
        parameters = (limit,)
    else:
        parameters = ()

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()

    records = []

    for row in rows:
        records.append({
            "id": row["id"],
            "operation": row["operation"],
            "input": json.loads(row["input_data"]),
            "result": json.loads(row["result"]),
            "created_at": row["created_at"],
        })

    return records


def get_record(record_id: int) -> dict | None:
    """Retrieve one record by database ID."""

    initialize_database()

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM analysis_history WHERE id = ?",
            (record_id,),
        ).fetchone()

    if row is None:
        return None

    return {
        "id": row["id"],
        "operation": row["operation"],
        "input": json.loads(row["input_data"]),
        "result": json.loads(row["result"]),
        "created_at": row["created_at"],
    }


def delete_record(record_id: int) -> bool:
    """Delete a record by ID."""

    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM analysis_history WHERE id = ?",
            (record_id,),
        )

        return cursor.rowcount > 0


def clear_records() -> int:
    """Delete all records and return the deleted count."""

    initialize_database()

    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM analysis_history"
        )

        return cursor.rowcount


def get_record_count() -> int:
    """Return total number of saved records."""

    initialize_database()

    with get_connection() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM analysis_history"
        ).fetchone()

    return result[0]


__all__ = [
    "get_connection",
    "initialize_database",
    "save_record",
    "get_records",
    "get_record",
    "delete_record",
    "clear_records",
    "get_record_count",
]
