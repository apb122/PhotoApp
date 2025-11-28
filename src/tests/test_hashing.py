from pathlib import Path

from src.core.hashing import hash_file


def test_hash_file(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello")
    assert hash_file(file_path) == hash_file(file_path)
