"""Small helper utilities."""
from __future__ import annotations

from pathlib import Path


def is_supported(path: Path, extensions: set[str]) -> bool:
    return path.suffix.lower() in extensions
