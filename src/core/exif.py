"""EXIF and metadata extraction helpers."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from PIL import Image, ExifTags


DATETIME_KEYS = {"DateTimeOriginal", "DateTime"}


def read_exif(path: Path) -> Dict[str, Any]:
    """Read EXIF metadata from an image file."""
    with Image.open(path) as img:
        raw = img._getexif() or {}
    decoded = {}
    for tag, value in raw.items():
        name = ExifTags.TAGS.get(tag, str(tag))
        decoded[name] = value
    return decoded


def parse_taken_at(exif: Dict[str, Any]) -> datetime | None:
    for key in DATETIME_KEYS:
        value = exif.get(key)
        if not value:
            continue
        try:
            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except (ValueError, TypeError):
            continue
    return None
