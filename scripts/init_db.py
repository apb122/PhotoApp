"""Initialize the SQLite database schema."""
from __future__ import annotations

from pathlib import Path

from src.core.config import load_config
from src.core.db import init_database


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    config = load_config(repo_root)
    init_database(config)
    print(f"Initialized DB at {config.database_path}")
