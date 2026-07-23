import io
from unittest.mock import mock_open, patch


class TestPredict:
    def test_requires_auth(self, client):
        response = client.post("/predict", data={"model_name": "DenseNet121"},
                               files={"file": ("test.jpg", io.BytesIO(b"fake"), "image/jpeg")})
        assert response.status_code == 401

    def test_successful_prediction(self, client, mock_db_connection, mock_ml_engine,
                                   mock_xai_generator, mock_pdf_generator):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = [0]
        cursor.fetchall.return_value = []
        client.cookies.set("session_token", "1")

        image_content = io.BytesIO(b"fake_image_data")
        with patch("builtins.open", mock_open(read_data=b"fake")), \
             patch("shutil.copyfileobj"):
            response = client.post("/predict", data={"model_name": "DenseNet121"},
                                   files={"file": ("test_xray.jpg", image_content, "image/jpeg")})
            assert response.status_code == 200, f"Got {response.status_code}: {response.text[:500]}"
            data = response.json()
            assert data["status"] == "success"
            assert data["label"] == "Neumonía"
            assert data["confidence"] == 85.0

    def test_returns_500_on_prediction_error(self, client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = [0]
        client.cookies.set("session_token", "1")
        with patch("routers.inference.process_and_predict", side_effect=Exception("Model crash")):
            response = client.post("/predict", data={"model_name": "DenseNet121"},
                                   files={"file": ("bad.jpg", io.BytesIO(b"x"), "image/jpeg")})
            assert response.status_code == 500
