

class TestQueueStatus:
    def test_requires_auth(self, client):
        response = client.get("/api/queue/status")
        assert response.status_code == 401

    def test_returns_empty_when_no_jobs(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchall.return_value = []
        cursor.fetchone.return_value = None
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/queue/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["has_pending"] is False
        assert len(data["jobs"]) == 0

    def test_returns_queued_jobs(self, client, mock_db_connection):
        from datetime import datetime

        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchall.return_value = [
            {"id": 1, "user_id": 1, "job_type": "diagnosis", "status": "queued",
             "payload": '{"model_name": "DenseNet121", "image_path": "img.jpg"}',
             "created_at": datetime(2026, 7, 29, 10, 0, 0),
             "started_at": None, "finished_at": None, "error_message": None},
            {"id": 2, "user_id": 1, "job_type": "training", "status": "running",
             "payload": '{"session_id": "RUN_001", "models": ["ResNet50"]}',
             "created_at": datetime(2026, 7, 29, 10, 1, 0),
             "started_at": datetime(2026, 7, 29, 10, 2, 0),
             "finished_at": None, "error_message": None},
        ]
        cursor.fetchone.return_value = {"pos": 0}
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/api/queue/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["has_pending"] is True
        assert len(data["jobs"]) == 2
        assert data["jobs"][0]["job_type"] == "diagnosis"
        assert data["jobs"][0]["model_name"] == "DenseNet121"
        assert data["jobs"][1]["job_type"] == "training"
        assert data["jobs"][1]["session_id"] == "RUN_001"


class TestQueueCancel:
    def test_requires_auth(self, client):
        response = client.delete("/api/queue/cancel/1")
        assert response.status_code == 401

    def test_cancels_queued_job(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.rowcount = 1
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.delete("/api/queue/cancel/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_returns_404_for_nonexistent(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.rowcount = 0
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.delete("/api/queue/cancel/999")
        assert response.status_code == 404
