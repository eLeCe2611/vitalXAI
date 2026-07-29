import io
from unittest.mock import mock_open, patch


class TestPredict:
    def test_requires_auth(self, client):
        response = client.post("/predict", data={"model_name": "DenseNet121"},
                               files={"file": ("test.jpg", io.BytesIO(b"fake"), "image/jpeg")})
        assert response.status_code == 401

    def test_successful_prediction(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"pos": 0}
        cursor.lastrowid = 1
        token = create_access_token(1)
        client.cookies.set("access_token", token)

        image_content = io.BytesIO(b"fake_image_data")
        with patch("builtins.open", mock_open(read_data=b"fake")), \
             patch("shutil.copyfileobj"):
            response = client.post("/predict", data={"model_name": "DenseNet121"},
                                   files={"file": ("test_xray.jpg", image_content, "image/jpeg")})
            assert response.status_code == 200, f"Got {response.status_code}: {response.text[:500]}"
            data = response.json()
            assert data["status"] == "queued"
            assert "job_id" in data

    def test_returns_queued_on_success(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"pos": 0}
        cursor.lastrowid = 42
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        with patch("builtins.open", mock_open(read_data=b"fake")), \
             patch("shutil.copyfileobj"):
            response = client.post("/predict", data={"model_name": "DenseNet121"},
                                   files={"file": ("xray.jpg", io.BytesIO(b"x"), "image/jpeg")})
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "queued"
            assert data["job_id"] == 42
