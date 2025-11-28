from pathlib import Path

from src.core.exif import parse_taken_at


def test_parse_taken_at_none():
    assert parse_taken_at({}) is None
