import json
from unittest.mock import mock_open, patch


class TestVerifySessionOwnership:
    def test_returns_true_when_user_owns_session(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=json.dumps({"user_id": 1}))):
            from services.mlops_engine import _verify_session_ownership
            assert _verify_session_ownership("session_1", 1) is True

    def test_returns_false_when_user_does_not_own_session(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=json.dumps({"user_id": 1}))):
            from services.mlops_engine import _verify_session_ownership
            assert _verify_session_ownership("session_1", 2) is False

    def test_returns_false_when_session_not_found(self):
        with patch("os.path.exists", return_value=False):
            from services.mlops_engine import _verify_session_ownership
            assert _verify_session_ownership("ghost", 1) is False

    def test_returns_false_when_config_has_no_user_id(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=json.dumps({"epochs": 10}))):
            from services.mlops_engine import _verify_session_ownership
            assert _verify_session_ownership("legacy", 1) is False


class TestCreateTrainingSession:
    def test_stores_user_id_in_config(self):
        with patch("os.makedirs") as mock_makedirs, \
             patch("builtins.open", mock_open()) as mock_file, \
             patch("json.dump") as mock_json_dump:
            from services.mlops_engine import create_training_session
            session_id = create_training_session("DenseNet121", "/data", 10, 32, 0.001, user_id=5)
            assert session_id.startswith("RUN_")
            call_args = mock_json_dump.call_args[0][0]
            assert call_args["user_id"] == 5
            assert call_args["models"] == ["DenseNet121"]
            assert call_args["dataset_path"] == "/data"


class TestBrowseFolder:
    def test_returns_demo_dataset_when_env_set(self, monkeypatch):
        monkeypatch.setenv("TFG_DEMO_DATASET", "C:/demo/Images")
        monkeypatch.delenv("TFG_DEMO_EXTERNAL_DATASET", raising=False)
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory") as ask:
            assert browse_folder() == {"path": "C:/demo/Images"}
            ask.assert_not_called()

    def test_returns_external_dataset_when_env_set(self, monkeypatch):
        monkeypatch.setenv("TFG_DEMO_EXTERNAL_DATASET", "C:/demo/ExternalDataset")
        monkeypatch.delenv("TFG_DEMO_DATASET", raising=False)
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory") as ask:
            assert browse_folder(for_external=True) == {"path": "C:/demo/ExternalDataset"}
            ask.assert_not_called()

    def test_training_browse_ignores_external_var(self, monkeypatch):
        monkeypatch.setenv("TFG_DEMO_EXTERNAL_DATASET", "C:/demo/ExternalDataset")
        monkeypatch.delenv("TFG_DEMO_DATASET", raising=False)
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory", return_value="C:/picked"):
            assert browse_folder() == {"path": "C:/picked"}

    def test_external_browse_ignores_training_var(self, monkeypatch):
        monkeypatch.setenv("TFG_DEMO_DATASET", "C:/demo/Images")
        monkeypatch.delenv("TFG_DEMO_EXTERNAL_DATASET", raising=False)
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory", return_value="C:/picked"):
            assert browse_folder(for_external=True) == {"path": "C:/picked"}

    def test_both_vars_set_select_by_for_external(self, monkeypatch):
        monkeypatch.setenv("TFG_DEMO_DATASET", "C:/demo/Images")
        monkeypatch.setenv("TFG_DEMO_EXTERNAL_DATASET", "C:/demo/ExternalDataset")
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory") as ask:
            assert browse_folder() == {"path": "C:/demo/Images"}
            assert browse_folder(for_external=True) == {"path": "C:/demo/ExternalDataset"}
            ask.assert_not_called()

    def test_falls_back_to_tkinter_dialog_without_demo_vars(self, monkeypatch):
        monkeypatch.delenv("TFG_DEMO_DATASET", raising=False)
        monkeypatch.delenv("TFG_DEMO_EXTERNAL_DATASET", raising=False)
        from services.mlops_engine import browse_folder
        with patch("services.mlops_engine.tk.Tk"), \
             patch("services.mlops_engine.filedialog.askdirectory", return_value="C:/picked"):
            assert browse_folder() == {"path": "C:/picked"}

