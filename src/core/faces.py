"""Face detection and embedding utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import numpy as np


@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]
    quality: float
    embedding: np.ndarray


class FaceEmbedder:
    """Thin wrapper around an InsightFace model."""

    def __init__(self, model_path: Path):
        self.model_path = model_path
        # Lazy load real model later

    def detect_and_embed(self, image_path: Path) -> List[DetectedFace]:
        # Placeholder for real detection logic
        _ = image_path
        return []
