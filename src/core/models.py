"""SQLAlchemy ORM models for the photo manager domain."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Root(Base):
    """Represents a configured root directory that contains photos."""

    __tablename__ = "roots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    photos: Mapped[list["Photo"]] = relationship(
        "Photo", back_populates="root", cascade="all, delete-orphan"
    )


class Photo(Base):
    """Represents a photo file tracked by the application."""

    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    root_id: Mapped[int] = mapped_column(ForeignKey("roots.id"), nullable=False, index=True)
    relative_path: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_hash: Mapped[str | None] = mapped_column(String, index=True)
    filesize: Mapped[int | None] = mapped_column(Integer)
    mtime: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    taken_at: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    rating: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    orientation: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    thumb_status: Mapped[str] = mapped_column(String, default="none", nullable=False)

    root: Mapped[Root] = relationship("Root", back_populates="photos")
    exif: Mapped["ExifData" | None] = relationship(
        "ExifData", back_populates="photo", cascade="all, delete-orphan", uselist=False
    )
    photo_tags: Mapped[list["PhotoTag"]] = relationship(
        "PhotoTag", back_populates="photo", cascade="all, delete-orphan"
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary="photo_tags", back_populates="photos"
    )


class ExifData(Base):
    """Stores Exif metadata extracted from a photo file."""

    __tablename__ = "exif_data"

    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id"), primary_key=True, autoincrement=False
    )
    camera_make: Mapped[str | None] = mapped_column(String)
    camera_model: Mapped[str | None] = mapped_column(String)
    lens_model: Mapped[str | None] = mapped_column(String)
    iso: Mapped[int | None] = mapped_column(Integer)
    f_number: Mapped[float | None] = mapped_column(Float)
    exposure_time: Mapped[str | None] = mapped_column(String)
    focal_length: Mapped[float | None] = mapped_column(Float)
    gps_lat: Mapped[float | None] = mapped_column(Float)
    gps_lon: Mapped[float | None] = mapped_column(Float)
    original_datetime: Mapped[datetime | None] = mapped_column(DateTime)

    photo: Mapped[Photo] = relationship("Photo", back_populates="exif")


class Tag(Base):
    """Represents a descriptive tag that can be assigned to photos."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    photo_tags: Mapped[list["PhotoTag"]] = relationship(
        "PhotoTag", back_populates="tag", cascade="all, delete-orphan"
    )
    photos: Mapped[list[Photo]] = relationship(
        "Photo", secondary="photo_tags", back_populates="tags"
    )


class PhotoTag(Base):
    """Association table linking photos to tags."""

    __tablename__ = "photo_tags"
    __table_args__ = (UniqueConstraint("photo_id", "tag_id", name="uq_photo_tag"),)

    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id"), primary_key=True, autoincrement=False
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id"), primary_key=True, autoincrement=False
    )

    photo: Mapped[Photo] = relationship("Photo", back_populates="photo_tags")
    tag: Mapped[Tag] = relationship("Tag", back_populates="photo_tags")
