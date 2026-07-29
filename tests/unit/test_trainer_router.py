import json
from unittest.mock import MagicMock, mock_open, patch

from services.auth_service import create_access_token


def _auth(client, user_id=1):
    token = create_access_token(user_id)
    client.cookies.set("access_token", token)
    return client


def _owning():
    return patch("services.mlops_engine._verify_session_ownership", return_value=True)


def _not_owning():
    return patch("services.mlops_engine._verify_session_ownership", return_value=False)


class TestAuth:
    def test_all_endpoints_return_401_without_token(self, client):
        endpoints = [
            ("POST", "/api/chat", {"session_id": "s", "message": "hi"}),
            ("GET", "/api/train/browse", None),
            ("POST", "/api/train/start", {"model_names": "m", "dataset_path": "/d", "epochs": 1, "batch_size": 1, "learning_rate": 0.01}),
            ("GET", "/api/train/logs", None),
            ("GET", "/api/train/models", None),
            ("GET", "/api/train/results/s/m", None),
            ("POST", "/api/train/run_eval", {"session_id": "s", "model_name": "m"}),
            ("DELETE", "/api/train/session/s", None),
            ("POST", "/api/train/session/rename", {"old_name": "o", "new_name": "n"}),
            ("POST", "/api/train/session/compare", {"session_id": "s"}),
            ("GET", "/api/train/session/s/ranking", None),
            ("POST", "/api/train/session/external_validation", {"session_id": "s", "dataset_path": "/d"}),
            ("GET", "/api/train/session/s/external_results", None),
            ("GET", "/api/train/session/s/report", None),
        ]
        for method, path, data in endpoints:
            if method == "POST":
                resp = client.post(path, data=data or {})
            elif method == "DELETE":
                resp = client.delete(path)
            else:
                resp = client.get(path)
            assert resp.status_code == 401, f"{method} {path} expected 401, got {resp.status_code}"


class TestChat:
    def test_new_session_creates_conversation(self, client):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="¡Hola! ¿Qué modelos quieres usar?"))
        ]
        _auth(client)
        with patch("services.chatbot_service.client", mock_client):
            response = client.post("/api/chat",
                                   data={"session_id": "test_1", "message": "Hola"})
            assert response.status_code == 200
            data = response.json()
            assert "response" in data

    def test_existing_session_reuses_conversation(self, client):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="1"))
        ]
        _auth(client)
        with patch("services.chatbot_service.client", mock_client):
            client.post("/api/chat", data={"session_id": "test_2", "message": "Hola"})
            mock_client.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="2"))
            ]
            response = client.post("/api/chat", data={"session_id": "test_2", "message": "Adiós"})
            assert response.status_code == 200

    def test_handles_groq_error(self, client):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Key invalid")
        _auth(client)
        with patch("services.chatbot_service.client", mock_client):
            response = client.post("/api/chat",
                                   data={"session_id": "test_3", "message": "Hola"})
            assert response.status_code == 500
            data = response.json()
            assert "API Key" in data["response"]


class TestBrowseFolder:
    def test_returns_selected_path(self, client):
        _auth(client)
        with patch("services.mlops_engine.tk.Tk") as mock_tk, \
             patch("services.mlops_engine.filedialog.askdirectory", return_value="C:/dataset"):
            response = client.get("/api/train/browse")
            assert response.status_code == 200
            assert response.json()["path"] == "C:/dataset"


class TestStartTraining:
    def test_starts_training_with_valid_params(self, client, mock_db_connection):
        _auth(client)
        cursor = mock_db_connection["cursor"]
        cursor.lastrowid = 99
        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", mock_open()), \
             patch("json.dump"):
            response = client.post("/api/train/start", data={
                "model_names": "DenseNet121,ResNet50",
                "dataset_path": "C:/dataset",
                "epochs": 20, "batch_size": 32, "learning_rate": 0.001
            })
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "queued"
            assert data["job_id"] == 99

    def test_rejects_invalid_dataset_path(self, client):
        _auth(client)
        with patch("os.path.exists", return_value=False):
            response = client.post("/api/train/start", data={
                "model_names": "DenseNet121",
                "dataset_path": "C:/fake",
                "epochs": 10, "batch_size": 16, "learning_rate": 0.01
            })
            assert response.status_code == 400


class TestGetLogs:
    def test_returns_logs_when_file_exists(self, client):
        _auth(client)
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data="line1\nline2\nline3")):
            response = client.get("/api/train/logs")
            assert response.status_code == 200
            assert "line1" in response.json()["logs"]

    def test_returns_placeholder_when_no_logs(self, client):
        _auth(client)
        with patch("os.path.exists", return_value=False):
            response = client.get("/api/train/logs")
            assert response.status_code == 200
            assert response.json()["logs"] == "Esperando..."


class TestGetModels:
    def test_returns_sessions_with_models(self, client):
        _auth(client)
        fake_config = json.dumps({"user_id": 1})
        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=["RUN_20260101_120000"]), \
             patch("os.path.isdir", return_value=True), \
             patch("os.path.exists") as mock_exists, \
             patch("builtins.open", mock_open(read_data=fake_config)):
            mock_exists.side_effect = lambda p: p.endswith("kfold_results.csv") or p.startswith("training_results")
            response = client.get("/api/train/models")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert len(data["sessions"]) == 1
            assert data["sessions"][0]["session_id"] == "RUN_20260101_120000"


class TestSessionResults:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.get("/api/train/results/fake_session/fake_model")
            assert response.status_code == 403

    def test_returns_404_for_missing_results(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=False):
            response = client.get("/api/train/results/fake_session/fake_model")
            assert response.status_code == 404


class TestRunEval:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.post("/api/train/run_eval", data={"session_id": "s", "model_name": "m"})
            assert response.status_code == 403

    def test_missing_dataset_returns_error(self, client, mock_db_connection):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=False):
            response = client.post("/api/train/run_eval",
                                   data={"session_id": "s1", "model_name": "m1"})
            assert response.status_code == 400


class TestSessionMgmt:
    def test_delete_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.delete("/api/train/session/RUN_20260101")
            assert response.status_code == 403

    def test_delete_existing_session(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=True), \
                 patch("shutil.rmtree") as mock_rmtree:
            response = client.delete("/api/train/session/RUN_20260101")
            assert response.status_code == 200
            mock_rmtree.assert_called_once()

    def test_delete_nonexistent_session(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=False):
            response = client.delete("/api/train/session/ghost")
            assert response.status_code == 404

    def test_rename_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "MySession"})
            assert response.status_code == 403

    def test_rename_session_success(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists") as mock_exists, \
                 patch("os.rename") as mock_rename:
            mock_exists.side_effect = lambda p: "RUN_OLD" in p and "MySession" not in p
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "MySession"})
            assert response.status_code == 200
            data = response.json()
            assert data["new_name"] == "MySession"

    def test_rename_to_existing_name(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=True):
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "Existing"})
            assert response.status_code == 400


class TestCompare:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.post("/api/train/session/compare", data={"session_id": "s"})
            assert response.status_code == 403


class TestRanking:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.get("/api/train/session/s/ranking")
            assert response.status_code == 403


class TestExtValidation:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.post("/api/train/session/external_validation",
                                   data={"session_id": "s", "dataset_path": "/d"})
            assert response.status_code == 403


class TestExtResults:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning():
            response = client.get("/api/train/session/s/external_results")
            assert response.status_code == 403


class TestReportEndpoint:
    def test_returns_403_for_unowned_session(self, client, mock_db_connection):
        _auth(client)
        mock_db_connection["cursor"].fetchone.return_value = {"role": "doctor"}
        with _not_owning(), patch("os.path.exists", return_value=False):
            response = client.get("/api/train/session/s/report")
            assert response.status_code == 403

    def test_returns_404_for_missing_session(self, client):
        _auth(client)
        with _owning(), patch("os.path.exists", return_value=False):
            response = client.get("/api/train/session/fake/report")
            assert response.status_code == 404

    def test_returns_pdf_for_valid_session(self, client):
        _auth(client)
        with _owning():
            import json as real_json
            import os as _os
            session_dir = "training_results/s1"
            _os.makedirs(session_dir, exist_ok=True)
            cfg_path = _os.path.join(session_dir, "config.json")
            csv_path = _os.path.join(session_dir, "session_ranking.csv")
            with open(cfg_path, "w") as f:
                real_json.dump({"dataset_path": "/data", "epochs": 20, "batch_size": 32, "learning_rate": 0.001, "models": ["m1"]}, f)
            with open(csv_path, "w") as f:
                f.write("Model,Mean,Std\nm1,0.95,0.02\n")

            response = client.get("/api/train/session/s1/report")
            assert response.status_code == 200

            import shutil
            shutil.rmtree("training_results/s1", ignore_errors=True)


class TestGroqApiKey:
    """Tests for GROQ_API_KEY environment variable usage."""

    def test_groq_api_key_reads_from_env(self):
        """GROQ_API_KEY must be read from environment, not hardcoded."""
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {"GROQ_API_KEY": "test-groq-key-from-env"}):
            import importlib

            import services.chatbot_service
            importlib.reload(services.chatbot_service)

            assert services.chatbot_service.GROQ_API_KEY == "test-groq-key-from-env"

        # Restore original env + module state
        importlib.reload(services.chatbot_service)
