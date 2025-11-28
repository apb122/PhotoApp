"""Generic image I/O helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image


def load_image(path: Path) -> Image.Image:
    return Image.open(path)


def save_image(image: Image.Image, path: Path, format: str = "JPEG") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format=format)


def get_size(path: Path) -> Tuple[int, int]:
    with Image.open(path) as img:
        return img.size
