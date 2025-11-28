"""Filesystem scanning utilities for photo roots."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from src.core.config import AppConfig
from src.core.models import Photo, Root


def _normalize_extensions(extensions: Iterable[str]) -> set[str]:
    return {ext.lower() for ext in extensions}


def _iter_photo_files(root_path: Path, extensions: set[str]) -> Iterable[Path]:
    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensions:
            continue
        yield path


def _relative_posix_path(path: Path, base: Path) -> str:
    return path.relative_to(base).as_posix()


def scan_root(root: Root, config: AppConfig, session: Session) -> None:
    """Scan a root directory and sync photo records in the database."""

    base_path = Path(root.path)
    if not base_path.is_dir():
        return

    extensions = _normalize_extensions(config.supported_extensions)

    existing_photos = session.query(Photo).filter_by(root_id=root.id).all()
    photos_by_relpath = {photo.relative_path: photo for photo in existing_photos}
    seen_paths: set[str] = set()

    for file_path in _iter_photo_files(base_path, extensions):
        relative_path = _relative_posix_path(file_path, base_path)
        seen_paths.add(relative_path)

        stat = file_path.stat()
        filesize = stat.st_size
        mtime = int(stat.st_mtime)

        photo = photos_by_relpath.get(relative_path)
        if photo is None:
            session.add(
                Photo(
                    root_id=root.id,
                    relative_path=relative_path,
                    filename=file_path.name,
                    filesize=filesize,
                    mtime=mtime,
                    status="active",
                    imported_at=datetime.utcnow(),
                    thumb_status="none",
                )
            )
        else:
            photo.filesize = filesize
            photo.mtime = mtime
            if photo.status == "missing":
                photo.status = "active"

    for photo in existing_photos:
        if photo.relative_path not in seen_paths:
            photo.status = "missing"
