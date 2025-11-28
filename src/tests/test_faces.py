from src.core.faces import FaceEmbedder


def test_embedder_init(tmp_path):
    embedder = FaceEmbedder(tmp_path / "model.onnx")
    assert embedder.model_path.exists() is False or embedder.model_path == tmp_path / "model.onnx"
