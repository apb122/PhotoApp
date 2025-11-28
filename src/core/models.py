"""Domain models for the photo manager."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Root:
    id: int
    path: Path
    name: str
    enabled: bool = True


@dataclass
class Photo:
    id: int
    root_id: int
    relative_path: Path
    filename: str
    file_hash: str | None = None
    filesize: int | None = None
    mtime: int | None = None
    status: str = "active"
    taken_at: Optional[datetime] = None
    imported_at: Optional[datetime] = None
    rating: int = 0
    favorite: bool = False
    orientation: int = 1
    thumb_status: str = "none"


@dataclass
class Face:
    id: int
    photo_id: int
    x: int
    y: int
    width: int
    height: int
    embedding: list[float] | None
    embedding_dim: int
    quality: float
    person_id: int | None = None
    cluster_id: int | None = None


@dataclass
class Person:
    id: int
    display_name: str
    notes: str | None = None
    merged_into_id: int | None = None
