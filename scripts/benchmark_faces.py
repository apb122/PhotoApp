"""Benchmark InsightFace embedding throughput."""
from __future__ import annotations

from pathlib import Path
from time import perf_counter

from src.core.faces import FaceEmbedder


if __name__ == "__main__":
    model_path = Path("data/models/w600k_r50.onnx")
    embedder = FaceEmbedder(model_path)
    start = perf_counter()
    _ = embedder.detect_and_embed(Path("/dev/null"))
    duration = perf_counter() - start
    print(f"Ran dummy embedding in {duration:.4f}s using model {model_path}")
