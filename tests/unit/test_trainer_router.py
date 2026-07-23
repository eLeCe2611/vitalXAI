from unittest.mock import MagicMock, mock_open, patch


class TestChat:
    def test_new_session_creates_conversation(self, client):
        with patch("routers.trainer.client.chat.completions.create") as mock_groq:
            mock_groq.return_value.choices = [
                MagicMock(message=MagicMock(content="¡Hola! ¿Qué modelos quieres usar?"))
            ]
            response = client.post("/api/chat",
                                   data={"session_id": "test_1", "message": "Hola"})
            assert response.status_code == 200
            data = response.json()
            assert "response" in data

    def test_existing_session_reuses_conversation(self, client):
        with patch("routers.trainer.client.chat.completions.create") as mock_groq:
            mock_groq.return_value.choices = [
                MagicMock(message=MagicMock(content="1"))
            ]
            client.post("/api/chat", data={"session_id": "test_2", "message": "Hola"})
            mock_groq.return_value.choices = [
                MagicMock(message=MagicMock(content="2"))
            ]
            response = client.post("/api/chat", data={"session_id": "test_2", "message": "Adiós"})
            assert response.status_code == 200

    def test_handles_groq_error(self, client):
        with patch("routers.trainer.client.chat.completions.create",
                   side_effect=Exception("API Key invalid")):
            response = client.post("/api/chat",
                                   data={"session_id": "test_3", "message": "Hola"})
            assert response.status_code == 500
            data = response.json()
            assert "API Key" in data["response"]


class TestBrowseFolder:
    def test_returns_selected_path(self, client):
        with patch("routers.trainer.tk.Tk") as mock_tk, \
             patch("routers.trainer.filedialog.askdirectory", return_value="C:/dataset"):
            response = client.get("/api/train/browse")
            assert response.status_code == 200
            assert response.json()["path"] == "C:/dataset"


class TestStartTraining:
    def test_starts_training_with_valid_params(self, client):
        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", mock_open()), \
             patch("json.dump"), \
             patch("routers.trainer.run_training_queue") as mock_run:
            response = client.post("/api/train/start", data={
                "model_names": "DenseNet121,ResNet50",
                "dataset_path": "C:/dataset",
                "epochs": 20, "batch_size": 32, "learning_rate": 0.001
            })
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            mock_run.assert_called_once()

    def test_rejects_invalid_dataset_path(self, client):
        with patch("os.path.exists", return_value=False):
            response = client.post("/api/train/start", data={
                "model_names": "DenseNet121",
                "dataset_path": "C:/fake",
                "epochs": 10, "batch_size": 16, "learning_rate": 0.01
            })
            assert response.status_code == 400


class TestGetLogs:
    def test_returns_logs_when_file_exists(self, client):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data="line1\nline2\nline3")):
            response = client.get("/api/train/logs")
            assert response.status_code == 200
            assert "line1" in response.json()["logs"]

    def test_returns_placeholder_when_no_logs(self, client):
        with patch("os.path.exists", return_value=False):
            response = client.get("/api/train/logs")
            assert response.status_code == 200
            assert response.json()["logs"] == "Esperando..."


class TestGetModels:
    def test_returns_sessions_with_models(self, client):
        with patch("os.path.exists", return_value=True), \
             patch("os.listdir", return_value=["RUN_20260101_120000"]), \
             patch("os.path.isdir", return_value=True), \
             patch("os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda p: p.endswith("kfold_results.csv") or p.startswith("training_results")
            response = client.get("/api/train/models")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"


class TestSessionResults:
    def test_returns_404_for_missing_results(self, client):
        with patch("os.path.exists", return_value=False):
            response = client.get("/api/train/results/fake_session/fake_model")
            assert response.status_code == 404


class TestRunEval:
    def test_missing_dataset_returns_error(self, client, mock_db_connection):
        with patch("os.path.exists", return_value=False):
            response = client.post("/api/train/run_eval",
                                   data={"session_id": "s1", "model_name": "m1"})
            assert response.status_code == 400


class TestSessionMgmt:
    def test_delete_existing_session(self, client):
        with patch("os.path.exists", return_value=True), \
             patch("shutil.rmtree") as mock_rmtree:
            response = client.delete("/api/train/session/RUN_20260101")
            assert response.status_code == 200
            mock_rmtree.assert_called_once()

    def test_delete_nonexistent_session(self, client):
        with patch("os.path.exists", return_value=False):
            response = client.delete("/api/train/session/ghost")
            assert response.status_code == 404

    def test_rename_session_success(self, client):
        with patch("os.path.exists") as mock_exists, \
             patch("os.rename") as mock_rename:
            mock_exists.side_effect = lambda p: "RUN_OLD" in p and "MySession" not in p
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "MySession"})
            assert response.status_code == 200
            data = response.json()
            assert data["new_name"] == "MySession"

    def test_rename_to_existing_name(self, client):
        with patch("os.path.exists", return_value=True):
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "Existing"})
            assert response.status_code == 400


class TestRunTrainingQueue:
    def test_executes_cnn_and_transformer_models(self):
        mock_process = MagicMock()
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("subprocess.Popen", return_value=mock_process) as mock_popen, \
             patch("os.path.join", side_effect=lambda *a: "/".join(a)), \
             patch("os.getcwd", return_value="/base"):
            from routers.trainer import run_training_queue
            run_training_queue(
                session_id="RUN_TEST",
                models=["DenseNet121", "deit"],
                dataset_path="/data",
                epochs=10, batch_size=32, learning_rate=0.001
            )
            # Should have called 4 subprocesses per model (train, xai_img, xai_math) + stats
            assert mock_popen.call_count >= 7

    def test_selects_correct_script_for_cnn(self):
        mock_process = MagicMock()
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("subprocess.Popen", return_value=mock_process) as mock_popen, \
             patch("os.path.join", side_effect=lambda *a: "/".join(a)), \
             patch("os.getcwd", return_value="/base"):
            from routers.trainer import run_training_queue
            run_training_queue(
                session_id="RUN_TEST", models=["DenseNet121"],
                dataset_path="/data", epochs=5, batch_size=16, learning_rate=0.01
            )
            # First call should use the CNN training script
            first_call = mock_popen.call_args_list[0]
            script_path = first_call[0][0][1]
            assert "1_train_kfold" in script_path

    def test_selects_correct_script_for_transformer(self):
        mock_process = MagicMock()
        with patch("builtins.open", mock_open()) as mock_file, \
             patch("subprocess.Popen", return_value=mock_process) as mock_popen, \
             patch("os.path.join", side_effect=lambda *a: "/".join(a)), \
             patch("os.getcwd", return_value="/base"):
            from routers.trainer import run_training_queue
            run_training_queue(
                session_id="RUN_TEST", models=["deit"],
                dataset_path="/data", epochs=5, batch_size=16, learning_rate=0.01
            )
            first_call = mock_popen.call_args_list[0]
            script_path = first_call[0][0][1]
            assert "2_train_transformer" in script_path


class TestReportEndpoint:
    def test_returns_404_for_missing_session(self, client):
        with patch("os.path.exists", return_value=False):
            response = client.get("/api/train/session/fake/report")
            assert response.status_code == 404

    def test_returns_pdf_for_valid_session(self, client):
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
        with patch("os.path.exists", return_value=True):
            response = client.post("/api/train/session/rename",
                                   data={"old_name": "RUN_OLD", "new_name": "Existing"})
            assert response.status_code == 400
