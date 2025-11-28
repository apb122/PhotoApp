"""Utilities for hashing and comparing files."""
from __future__ import annotations

import hashlib
from pathlib import Path


def compute_file_hash(path: Path, chunk_size: int = 1 << 20) -> str:
    """Compute a SHA-256 hash for the given file.

    Args:
        path: Path to the file to hash.
        chunk_size: Number of bytes to read per chunk.

    Returns:
        Hexadecimal SHA-256 digest of the file contents.
    """
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)

    return digest.hexdigest()


def files_are_equal(path1: Path, path2: Path) -> bool:
    """Determine whether two files are identical.

    Files are first compared by size and modification time to avoid
    unnecessary hashing. If both size and mtime match, a SHA-256 hash
    comparison is performed.

    Args:
        path1: Path to the first file.
        path2: Path to the second file.

    Returns:
        True if files match by size, mtime, and content hash; otherwise False.
    """
    stat1 = path1.stat()
    stat2 = path2.stat()

    if stat1.st_size != stat2.st_size:
        return False

    if stat1.st_mtime_ns != stat2.st_mtime_ns:
        return False

    return compute_file_hash(path1) == compute_file_hash(path2)
