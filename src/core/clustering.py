"""Clustering utilities for grouping faces into people."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np


@dataclass
class ClusterResult:
    cluster_id: int
    face_indices: List[int]


def cluster_embeddings(embeddings: Iterable[np.ndarray]) -> List[ClusterResult]:
    """Placeholder clustering strategy; replace with DBSCAN/HDBSCAN later."""
    _ = embeddings
    return []
