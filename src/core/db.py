"""SQLite database connection helpers."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator

from .config import Config


_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS roots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        name TEXT NOT NULL,
        enabled INTEGER NOT NULL DEFAULT 1
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        root_id INTEGER NOT NULL REFERENCES roots(id),
        relative_path TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_hash TEXT,
        filesize INTEGER,
        mtime INTEGER,
        status TEXT,
        taken_at TEXT,
        imported_at TEXT,
        rating INTEGER DEFAULT 0,
        favorite INTEGER DEFAULT 0,
        orientation INTEGER DEFAULT 1,
        thumb_status TEXT DEFAULT 'none'
    );
    """,
]


def get_connection(config: Config) -> sqlite3.Connection:
    database_path = Path(config.paths.database)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    for statement in _SCHEMA:
        conn.executescript(statement)
    conn.commit()


def iter_rows(cursor: sqlite3.Cursor) -> Iterator[sqlite3.Row]:
    while (row := cursor.fetchone()) is not None:
        yield row
