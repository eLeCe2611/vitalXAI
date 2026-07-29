

class TestAdminUsers:
    def test_requires_auth(self, client):
        response = client.get("/api/admin/users")
        assert response.status_code == 401

    def test_returns_403_for_non_admin(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"role": "doctor"}
        token = create_access_token(5)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/users")
        assert response.status_code == 403

    def test_returns_user_list_for_admin(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [
            {"role": "admin"},
            None,
        ]
        cursor.fetchall.return_value = [
            {"id": 1, "username": "admin", "first_name": "Luis", "last_name": "Carmona", "role": "admin", "diagnosis_count": 5, "lab_count": 2},
            {"id": 2, "username": "lgarcia", "first_name": "Laura", "last_name": "Garcia", "role": "doctor", "diagnosis_count": 0, "lab_count": 0},
        ]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/users")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["users"]) == 2
        assert data["users"][0]["username"] == "admin"


class TestAdminUserConsultations:
    def test_requires_auth(self, client):
        response = client.get("/api/admin/users/1/consultations")
        assert response.status_code == 401

    def test_returns_403_for_non_admin(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"role": "doctor"}
        token = create_access_token(5)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/users/1/consultations")
        assert response.status_code == 403

    def test_returns_consultations_for_admin(self, client, mock_db_connection):
        from datetime import datetime

        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [
            {"role": "admin"},
            {"id": 2, "username": "lgarcia"},
        ]
        cursor.fetchall.side_effect = [
            [
                {"id": 1, "user_id": 2, "timestamp": datetime(2026, 7, 23, 10, 0, 0),
                 "model_name": "DenseNet121", "original_image_path": "img.jpg",
                 "xai_image_path": "xai.jpg", "prediction_label": "Neumonia",
                 "confidence_score": 95.0, "patient_name": "Paciente X", "pdf_path": "report.pdf"}
            ],
            []
        ]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/users/2/consultations")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["consultations"]) == 1


class TestAdminGetConsultation:
    def test_requires_auth(self, client):
        response = client.get("/api/admin/consultations/1")
        assert response.status_code == 401

    def test_returns_403_for_non_admin(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"role": "doctor"}
        token = create_access_token(5)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/consultations/1")
        assert response.status_code == 403

    def test_returns_404_for_missing(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [{"role": "admin"}, None]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/consultations/999")
        assert response.status_code == 404

    def test_returns_consultation_for_admin(self, client, mock_db_connection):
        from datetime import datetime

        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [
            {"role": "admin"},
            {"id": 1, "user_id": 2, "timestamp": datetime(2026, 7, 23, 10, 0, 0),
             "model_name": "DenseNet121", "original_image_path": "img.jpg",
             "xai_image_path": "xai.jpg", "prediction_label": "Neumonia",
             "confidence_score": 95.0, "patient_name": "Paciente X", "pdf_path": "report.pdf"}
        ]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/admin/consultations/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["consultation"]["id"] == 1
