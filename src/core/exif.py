"""EXIF and metadata extraction helpers."""
from __future__ import annotations

import logging
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from PIL import ExifTags, Image, UnidentifiedImageError


ExifDict = Dict[str, Any]

_NORMALIZED_KEYS = [
    "camera_make",
    "camera_model",
    "lens_model",
    "iso",
    "f_number",
    "exposure_time",
    "focal_length",
    "gps_lat",
    "gps_lon",
    "original_datetime",
]


def _decode_exif(raw_exif: Any) -> ExifDict:
    decoded: ExifDict = {}
    if not raw_exif:
        return decoded
    for tag, value in raw_exif.items():
        name = ExifTags.TAGS.get(tag, str(tag))
        decoded[name] = value
    return decoded


def _first_existing(data: ExifDict, keys: Iterable[str]) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return None


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, Fraction):
        return float(value)
    if isinstance(value, tuple) and len(value) == 2 and all(isinstance(v, (int, float)) for v in value):
        denominator = value[1]
        if denominator:
            return float(value[0]) / float(denominator)
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(str(value), fmt)
        except (ValueError, TypeError):
            continue
    return None


def _rational_to_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}" if value.denominator else str(float(value))
    if isinstance(value, tuple) and len(value) == 2:
        numerator, denominator = value
        try:
            if denominator:
                frac = Fraction(numerator, denominator)
                return f"{frac.numerator}/{frac.denominator}"
            return str(float(numerator))
        except (TypeError, ValueError, ZeroDivisionError):
            return None
    try:
        return str(value)
    except Exception:  # noqa: BLE001
        return None


def _parse_gps(exif: ExifDict) -> Tuple[float | None, float | None]:
    gps_info = exif.get("GPSInfo")
    if not isinstance(gps_info, dict):
        return None, None

    decoded: Dict[str, Any] = {}
    for key, val in gps_info.items():
        name = ExifTags.GPSTAGS.get(key, str(key))
        decoded[name] = val

    lat = _convert_gps_coord(decoded.get("GPSLatitude"), decoded.get("GPSLatitudeRef"))
    lon = _convert_gps_coord(decoded.get("GPSLongitude"), decoded.get("GPSLongitudeRef"))
    return lat, lon


def _convert_gps_coord(coords: Any, ref: Any) -> float | None:
    if not coords or not ref:
        return None
    try:
        degrees, minutes, seconds = coords
        deg_val = _to_float(degrees) or 0.0
        min_val = _to_float(minutes) or 0.0
        sec_val = _to_float(seconds) or 0.0
        decimal = deg_val + (min_val / 60.0) + (sec_val / 3600.0)
        ref_str = str(ref).upper()
        if ref_str in {"S", "W"}:
            decimal = -decimal
        return decimal
    except (ValueError, TypeError):
        logging.debug("Failed to convert GPS coordinates", exc_info=True)
        return None


def extract_exif(path: Path) -> dict[str, Any]:
    """Extract and normalize EXIF data from an image file."""

    normalized: dict[str, Any] = {key: None for key in _NORMALIZED_KEYS}
    try:
        with Image.open(path) as img:
            raw_exif = img.getexif()
            exif_data = _decode_exif(raw_exif)
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        logging.warning("Unable to open image for EXIF extraction: %s", path, exc_info=True)
        return normalized

    normalized["camera_make"] = _first_existing(exif_data, ["Make"])
    normalized["camera_model"] = _first_existing(exif_data, ["Model"])
    normalized["lens_model"] = _first_existing(exif_data, ["LensModel", "LensMake"])

    normalized["iso"] = _first_existing(exif_data, ["PhotographicSensitivity", "ISOSpeedRatings"])
    normalized["f_number"] = _to_float(_first_existing(exif_data, ["FNumber"]))
    normalized["exposure_time"] = _rational_to_str(_first_existing(exif_data, ["ExposureTime"]))
    normalized["focal_length"] = _to_float(_first_existing(exif_data, ["FocalLength"]))

    original_dt = _parse_datetime(_first_existing(exif_data, ["DateTimeOriginal", "DateTime"]))
    normalized["original_datetime"] = original_dt

    gps_lat, gps_lon = _parse_gps(exif_data)
    normalized["gps_lat"] = gps_lat
    normalized["gps_lon"] = gps_lon

    return normalized


def guess_taken_at(path: Path, exif_data: dict[str, Any]) -> datetime | None:
    """Guess when a photo was taken using EXIF data or file metadata."""

    original_dt = exif_data.get("original_datetime")
    if isinstance(original_dt, datetime):
        return original_dt

    try:
        timestamp = path.stat().st_mtime
        return datetime.fromtimestamp(timestamp)
    except (OSError, FileNotFoundError):
        logging.debug("Failed to read file modification time for %s", path, exc_info=True)
        return None
