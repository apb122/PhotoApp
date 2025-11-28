"""High-level indexing pipeline tying together scan, EXIF, and thumbnails."""
from __future__ import annotations

from pathlib import Path

from src.core.config import Config
from src.core.exif import parse_taken_at, read_exif
from src.core.thumbnails import build_thumbnails
from src.services.scanner import Scanner


class Indexer:
    def __init__(self, config: Config):
        self.config = config
        self.scanner = Scanner(config)

    def index_root(self, root_path: Path) -> None:
        for path in self.scanner.scan_root(root_path):
            exif = read_exif(path)
            _taken_at = parse_taken_at(exif)
            # Insert into DB later
            build_thumbnails(self.config, photo_id=0, source=path)
