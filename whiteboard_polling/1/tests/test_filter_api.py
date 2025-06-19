from fastapi.testclient import TestClient
from backend.app import app
from config import ROOM_ID

client = TestClient(app)

def test_filter_invert():
    payload = {
        "image_data": [0, 0, 0, 255],  # чорний піксель
        "filter_name": "invert",
        "width": 1,
        "height": 1
    }

    response = client.post(f"/filter/{ROOM_ID}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "image_data" in data
    assert isinstance(data["image_data"], list)

    # Очікуємо інверсію: (255, 255, 255, 255)
    assert data["image_data"] == [255, 255, 255, 255]

