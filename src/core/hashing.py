"""File hashing utilities."""
from __future__ import annotations

import hashlib
from pathlib import Path


BUFFER_SIZE = 1024 * 1024


def hash_file(path: Path) -> str:
    """Return SHA-256 hash of file content."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(BUFFER_SIZE):
            digest.update(chunk)
    return digest.hexdigest()
