"""Search query helpers for retrieving photos."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from .models import Photo, PhotoTag, Tag


def _apply_common_filters(
    stmt: Select[tuple[Photo]],
    *,
    text: str | None,
    date_from: datetime | None,
    date_to: datetime | None,
    favorites_only: bool,
    root_ids: list[int] | None,
) -> Select[tuple[Photo]]:
    if text:
        stmt = stmt.where(Photo.filename.ilike(f"%{text}%"))

    if date_from:
        stmt = stmt.where(Photo.taken_at >= date_from)

    if date_to:
        stmt = stmt.where(Photo.taken_at <= date_to)

    if favorites_only:
        stmt = stmt.where(Photo.favorite.is_(True))

    if root_ids:
        stmt = stmt.where(Photo.root_id.in_(root_ids))

    return stmt


def query_photos(
    session: Session,
    text: str | None = None,
    tags: list[int] | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    favorites_only: bool = False,
    root_ids: list[int] | None = None,
    limit: int = 200,
    offset: int = 0,
) -> list[Photo]:
    """Return photos matching the provided search parameters."""

    stmt: Select[tuple[Photo]] = select(Photo)

    if tags:
        stmt = (
            stmt.join(PhotoTag, PhotoTag.photo_id == Photo.id)
            .join(Tag, Tag.id == PhotoTag.tag_id)
            .where(Tag.id.in_(tags))
            .distinct()
        )

    stmt = _apply_common_filters(
        stmt,
        text=text,
        date_from=date_from,
        date_to=date_to,
        favorites_only=favorites_only,
        root_ids=root_ids,
    )

    stmt = stmt.order_by(Photo.taken_at.desc(), Photo.id.desc())
    stmt = stmt.limit(limit).offset(offset)

    return list(session.scalars(stmt).all())
