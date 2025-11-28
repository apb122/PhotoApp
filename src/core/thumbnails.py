"""Thumbnail generation utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

from PIL import Image, ImageOps

from .config import AppConfig
from .models import Photo


VALID_SIZE_LABELS = {"small", "medium", "large"}


def _resolve_original_path(photo: Photo) -> Path:
    """Determine the absolute filesystem path for a photo's original image."""

    if photo.relative_path.is_absolute():
        return photo.relative_path

    root_path = getattr(photo, "root_path", None)
    root = getattr(photo, "root", None)
    if root_path is None and root is not None:
        root_path = getattr(root, "path", None)

    if root_path is None:
        raise ValueError("Photo instance must include a root path to resolve original file")

    return Path(root_path) / photo.relative_path


def get_thumbnail_path(photo_id: int, size_label: str, config: AppConfig) -> Path:
    """Compute the expected thumbnail path for a photo and size label."""

    _validate_size_label(size_label)
    return Path(config.cache_dir) / "thumbs" / f"{photo_id}_{size_label}.jpg"


def generate_thumbnail(photo: Photo, size_label: str, config: AppConfig) -> Path:
    """Generate a thumbnail for the given photo and size label, returning its path."""

    max_dimension = _get_max_dimension(size_label, config.thumb_sizes)
    source_path = _resolve_original_path(photo)
    if not source_path.exists():
        raise FileNotFoundError(f"Original image not found: {source_path}")

    destination = get_thumbnail_path(photo.id, size_label, config)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source_path) as image:
        oriented = ImageOps.exif_transpose(image)
        oriented.thumbnail((max_dimension, max_dimension))
        oriented.save(destination, format="JPEG")

    return destination


def ensure_thumbnails(photo: Photo, config: AppConfig, sizes: list[str] | None = None) -> Dict[str, Path]:
    """Ensure thumbnails for the specified sizes exist, generating any missing ones."""

    size_labels = _normalize_sizes(sizes, config.thumb_sizes)
    thumbnails: Dict[str, Path] = {}

    for label in size_labels:
        thumb_path = get_thumbnail_path(photo.id, label, config)
        if not thumb_path.exists():
            thumb_path = generate_thumbnail(photo, label, config)
        thumbnails[label] = thumb_path

    return thumbnails


def _normalize_sizes(sizes: Iterable[str] | None, available_sizes: Dict[str, int]) -> list[str]:
    if sizes is None:
        return list(available_sizes.keys())
    normalized = []
    for label in sizes:
        _validate_size_label(label)
        if label not in available_sizes:
            raise ValueError(f"Size label '{label}' is not configured")
        normalized.append(label)
    return normalized


def _get_max_dimension(size_label: str, sizes: Dict[str, int]) -> int:
    _validate_size_label(size_label)
    try:
        return int(sizes[size_label])
    except KeyError as exc:
        raise ValueError(f"Size label '{size_label}' is not configured") from exc


def _validate_size_label(size_label: str) -> None:
    if size_label not in VALID_SIZE_LABELS:
        raise ValueError(f"Invalid size label '{size_label}'. Must be one of {sorted(VALID_SIZE_LABELS)}")
