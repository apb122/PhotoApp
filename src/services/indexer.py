"""Indexing pipeline for extracting EXIF data and generating thumbnails."""
from __future__ import annotations

import logging
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, Iterable

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.core.config import AppConfig
from src.core.db import get_session
from src.core.exif import extract_exif, guess_taken_at
from src.core.models import ExifData, Photo
from src.core.thumbnails import ensure_thumbnails


logger = logging.getLogger(__name__)


def _resolve_photo_path(photo: Photo) -> tuple[SimpleNamespace, Path]:
    """Resolve the absolute file path for a photo and return a proxy for thumbnailing."""

    root_path_value = getattr(photo, "root_path", None)
    if root_path_value is None and photo.root is not None:
        root_path_value = photo.root.path

    if root_path_value is None:
        raise ValueError("Photo is missing root path information")

    root_path = Path(root_path_value)
    relative_path = Path(photo.relative_path)

    absolute_path = relative_path if relative_path.is_absolute() else root_path / relative_path

    proxy = SimpleNamespace(
        id=photo.id,
        relative_path=relative_path,
        root_path=root_path,
        root=photo.root,
    )
    return proxy, absolute_path


def _upsert_exif(session: Session, photo: Photo, exif_data: dict[str, object]) -> None:
    """Create or update the ExifData record for a photo."""

    record = photo.exif or ExifData(photo_id=photo.id)
    record.camera_make = exif_data.get("camera_make")
    record.camera_model = exif_data.get("camera_model")
    record.lens_model = exif_data.get("lens_model")
    record.iso = exif_data.get("iso")
    record.f_number = exif_data.get("f_number")
    record.exposure_time = exif_data.get("exposure_time")
    record.focal_length = exif_data.get("focal_length")
    record.gps_lat = exif_data.get("gps_lat")
    record.gps_lon = exif_data.get("gps_lon")
    record.original_datetime = exif_data.get("original_datetime")

    if photo.exif is None:
        session.add(record)
        photo.exif = record


def _process_photo(session: Session, photo: Photo, config: AppConfig) -> None:
    """Extract EXIF, update taken_at, and generate thumbnails for a single photo."""

    proxy, absolute_path = _resolve_photo_path(photo)
    exif_data = extract_exif(absolute_path)
    _upsert_exif(session, photo, exif_data)

    photo.taken_at = guess_taken_at(absolute_path, exif_data)

    ensure_thumbnails(proxy, config, sizes=["small"])
    photo.thumb_status = "ready"


def process_photos_in_batches(
    photos: Iterable[Photo],
    batch_size: int,
    processor: Callable[[Photo], None],
) -> None:
    """Process photos in batches, logging progress after each batch."""

    batch: list[Photo] = []
    processed = 0

    for photo in photos:
        batch.append(photo)
        if len(batch) >= batch_size:
            for item in batch:
                processor(item)
                processed += 1
            logger.info("Processed %s photos", processed)
            batch.clear()

    if batch:
        for item in batch:
            processor(item)
            processed += 1
        logger.info("Processed %s photos", processed)


def index_new_photos(config: AppConfig) -> None:
    """Index photos missing EXIF or thumbnails and update their metadata."""

    with get_session() as session:
        photos = (
            session.query(Photo)
            .filter(or_(Photo.thumb_status == "none", Photo.taken_at.is_(None)))
            .order_by(Photo.id)
            .all()
        )

        if not photos:
            logger.info("No photos require indexing")
            return

        def _handler(target: Photo) -> None:
            try:
                _process_photo(session, target, config)
            except Exception:  # noqa: BLE001
                logger.exception("Failed to index photo id=%s", target.id)
                target.thumb_status = "error"

        process_photos_in_batches(photos, batch_size=50, processor=_handler)
