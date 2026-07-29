from datetime import datetime


class TestGetHistory:
    def test_requires_auth(self, client):
        response = client.get("/api/history")
        assert response.status_code == 401

    def test_returns_consultations(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchall.return_value = [
            {"id": 1, "user_id": 1, "timestamp": datetime(2026, 7, 23, 10, 0, 0),
             "model_name": "DenseNet121", "original_image_path": "img.jpg",
             "xai_image_path": "xai.jpg", "prediction_label": "Neumon\u00eda",
             "confidence_score": 85.0, "patient_name": "Paciente X", "pdf_path": "report.pdf"}
        ]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/history")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["patient_name"] == "Paciente X"

    def test_empty_history(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchall.return_value = []
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/history")
        data = response.json()
        assert len(data["data"]) == 0


class TestUpdateName:
    def test_requires_auth(self, client):
        response = client.post("/api/history/update_name",
                               data={"consultation_id": 1, "new_name": "Juan"})
        assert response.status_code == 401

    def test_returns_403_for_unowned_consultation(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [{"user_id": 2}, {"role": "doctor"}]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.post("/api/history/update_name",
                               data={"consultation_id": 1, "new_name": "Juan"})
        assert response.status_code == 403

    def test_successful_update(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [{"user_id": 1}, {"role": "doctor"}]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.post("/api/history/update_name",
                               data={"consultation_id": 1, "new_name": "Juan P\u00e9rez"})
        assert response.status_code == 200
        assert response.json()["status"] == "success"


class TestDeleteRecord:
    def test_requires_auth(self, client):
        response = client.post("/api/history/delete", data={"consultation_id": 1})
        assert response.status_code == 401

    def test_returns_403_for_unowned_consultation(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [{"user_id": 2}, {"role": "doctor"}]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.post("/api/history/delete", data={"consultation_id": 1})
        assert response.status_code == 403

    def test_successful_deletion(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [{"user_id": 1}, {"role": "doctor"}]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.post("/api/history/delete", data={"consultation_id": 1})
        assert response.status_code == 200
        assert response.json()["status"] == "success"
