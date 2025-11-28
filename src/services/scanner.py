"""Filesystem scanning pipeline."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from src.core.config import Config
from src.core.hashing import hash_file
from src.core.utils import is_supported


class Scanner:
    def __init__(self, config: Config):
        self.config = config
        self.extensions = set(config.supported_extensions)

    def scan_root(self, root_path: Path) -> Iterable[Path]:
        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            if not is_supported(path, self.extensions):
                continue
            yield path

    def fingerprint(self, path: Path) -> tuple[str, int, float]:
        return hash_file(path), path.stat().st_size, path.stat().st_mtime
