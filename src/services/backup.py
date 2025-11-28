"""Backup and restore helpers."""
from __future__ import annotations

from pathlib import Path


def export_database(db_path: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(db_path.read_bytes())


def import_database(source: Path, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.write_bytes(source.read_bytes())
