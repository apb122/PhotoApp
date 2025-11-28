"""Configuration loading and access utilities."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field


class FaceRecognitionConfig(BaseModel):
    """Configuration options for face recognition workflows."""

    enabled: bool = Field(default=False)
    model_dir: Path = Field(..., description="Directory containing face recognition models")


class JobsConfig(BaseModel):
    """Settings controlling background job execution."""

    max_workers: int = Field(default=4, ge=1)


class AppConfig(BaseModel):
    """Top-level application configuration."""

    database_path: Path
    cache_dir: Path
    logs_dir: Path
    thumb_sizes: Dict[str, int]
    supported_extensions: list[str]
    face_recognition: FaceRecognitionConfig
    jobs: JobsConfig

    class Config:
        arbitrary_types_allowed = True


DEFAULT_CONFIG_PATH = Path("config/default.yaml")
USER_CONFIG_PATH = Path("config/user.yaml")


def _load_yaml(path: Path) -> Dict[str, Any]:
    """Safely load a YAML file, returning an empty dict when missing."""

    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries without mutating inputs."""

    merged: Dict[str, Any] = {**base}
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _find_repo_root() -> Path:
    """Locate the repository root by searching for the config directory."""

    current = Path(__file__).resolve()
    for ancestor in current.parents:
        if (ancestor / DEFAULT_CONFIG_PATH).exists():
            return ancestor
    raise FileNotFoundError("Could not locate repository root containing config/default.yaml")


def _resolve_path(value: str | Path, repo_root: Path) -> Path:
    """Convert a path value to an absolute path anchored at the repository root."""

    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (repo_root / candidate).resolve()


@lru_cache(maxsize=1)
def load_config() -> AppConfig:
    """Load and cache the application configuration."""

    repo_root = _find_repo_root()
    default_raw = _load_yaml(repo_root / DEFAULT_CONFIG_PATH)
    user_raw = _load_yaml(repo_root / USER_CONFIG_PATH)
    merged = _deep_merge(default_raw, user_raw)

    face_raw = merged.get("face_recognition", {})
    jobs_raw = merged.get("jobs", {})

    return AppConfig(
        database_path=_resolve_path(merged.get("database_path", "data/photos.db"), repo_root),
        cache_dir=_resolve_path(merged.get("cache_dir", "data/cache"), repo_root),
        logs_dir=_resolve_path(merged.get("logs_dir", "logs"), repo_root),
        thumb_sizes=dict(merged.get("thumb_sizes", {})),
        supported_extensions=list(merged.get("supported_extensions", [])),
        face_recognition=FaceRecognitionConfig(
            enabled=bool(face_raw.get("enabled", False)),
            model_dir=_resolve_path(face_raw.get("model_dir", "data/models/insightface"), repo_root),
        ),
        jobs=JobsConfig(max_workers=int(jobs_raw.get("max_workers", 4))),
    )
