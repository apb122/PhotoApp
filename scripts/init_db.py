"""Initialize the SQLite database schema."""
from __future__ import annotations

from pathlib import Path

from src.core.config import load_config
from src.core.db import ensure_schema, get_connection

if __name__ == "__main__":
    config = load_config(Path(__file__).resolve().parents[1])
    conn = get_connection(config)
    ensure_schema(conn)
    print(f"Initialized DB at {config.paths.database}")
