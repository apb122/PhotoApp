import numpy as np

from src.core.clustering import cluster_embeddings


def test_cluster_embeddings_empty():
    assert cluster_embeddings([]) == []
