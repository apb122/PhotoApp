from src.core.models import Photo


def test_photo_defaults():
    photo = Photo(id=1, root_id=1, relative_path="/a", filename="a.jpg")
    assert photo.status == "active"
