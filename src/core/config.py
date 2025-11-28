"""Configuration loading and access utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class Paths:
    database: Path
    cache_dir: Path
    models_dir: Path
    logs_dir: Path


@dataclass
class FaceModel:
    embedding_model: Path
    det_threshold: float
    max_batch: int


@dataclass
class UISettings:
    theme: str
    language: str
    auto_scan_on_startup: bool


@dataclass
class Config:
    paths: Paths
    thumb_sizes: Dict[str, int]
    supported_extensions: list[str]
    face_model: FaceModel
    ui: UISettings


_DEFAULT_CONFIG = "config/default.yaml"
_USER_CONFIG = "config/user.yaml"


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_config(project_root: Path) -> Config:
    """Load default + user config into a strongly-typed object."""
    default_raw = _load_yaml(project_root / _DEFAULT_CONFIG)
    user_raw = _load_yaml(project_root / _USER_CONFIG)
    merged = {**default_raw, **user_raw}

    paths_raw = merged.get("paths", {})
    paths = Paths(
        database=project_root / paths_raw.get("database", "data/db.sqlite3"),
        cache_dir=project_root / paths_raw.get("cache_dir", "data/cache"),
        models_dir=project_root / paths_raw.get("models_dir", "data/models"),
        logs_dir=project_root / paths_raw.get("logs_dir", "logs"),
    )

    face_raw = merged.get("face_model", {})
    face_model = FaceModel(
        embedding_model=paths.models_dir / face_raw.get("embedding_model", "models/model.onnx"),
        det_threshold=float(face_raw.get("det_threshold", 0.4)),
        max_batch=int(face_raw.get("max_batch", 16)),
    )

    ui_raw = merged.get("ui", {})
    ui = UISettings(
        theme=ui_raw.get("theme", "system"),
        language=ui_raw.get("language", "en"),
        auto_scan_on_startup=bool(ui_raw.get("auto_scan_on_startup", True)),
    )

    return Config(
        paths=paths,
        thumb_sizes=merged.get("thumb_sizes", {}),
        supported_extensions=merged.get("supported_extensions", []),
        face_model=face_model,
        ui=ui,
    )
