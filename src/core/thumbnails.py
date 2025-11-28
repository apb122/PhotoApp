"""Thumbnail generation utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

from PIL import Image

from .config import Config
from .image_io import save_image


def get_thumb_path(cache_dir: Path, photo_id: int, size_key: str) -> Path:
    return cache_dir / f"{photo_id}_{size_key}.jpg"


def ensure_thumbnail(source: Path, photo_id: int, sizes: Dict[str, int], cache_dir: Path) -> None:
    with Image.open(source) as img:
        for key, max_size in sizes.items():
            thumb = img.copy()
            thumb.thumbnail((max_size, max_size))
            save_image(thumb, get_thumb_path(cache_dir, photo_id, key))


def build_thumbnails(config: Config, photo_id: int, source: Path) -> None:
    cache_dir = Path(config.paths.cache_dir) / "thumbs"
    cache_dir.mkdir(parents=True, exist_ok=True)
    ensure_thumbnail(source, photo_id, config.thumb_sizes, cache_dir)
