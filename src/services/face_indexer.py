"""Service that runs face detection over photos."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from src.core.config import Config
from src.core.faces import FaceEmbedder


class FaceIndexer:
    def __init__(self, config: Config):
        self.embedder = FaceEmbedder(config.paths.models_dir / config.face_model.embedding_model)

    def index_faces(self, photos: Iterable[Path]) -> None:
        for photo_path in photos:
            detections = self.embedder.detect_and_embed(photo_path)
            _ = detections
            # Persist detections later
