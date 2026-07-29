import importlib.machinery
import secrets
import sys
import types
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

from main import app
from services.auth_service import create_access_token

# Create a proper mock module for cv2 to prevent OpenCV import errors
_mock_cv2_module = types.ModuleType("cv2")
_mock_cv2_spec = importlib.machinery.ModuleSpec("cv2", None, origin="mock")
_mock_cv2_module.__spec__ = _mock_cv2_spec
_mock_cv2 = MagicMock()
_mock_cv2.imread.return_value = np.zeros((224, 224, 3), dtype=np.uint8)
_mock_cv2.cvtColor.return_value = np.zeros((224, 224, 3), dtype=np.uint8)
_mock_cv2.resize.return_value = np.zeros((224, 224, 3), dtype=np.uint8)
_mock_cv2.COLOR_BGR2RGB = 4
_mock_cv2.IMREAD_COLOR = 1
for attr in ("imread", "cvtColor", "resize", "COLOR_BGR2RGB", "IMREAD_COLOR"):
    _mock_cv2_module.__dict__[attr] = getattr(_mock_cv2, attr)
if "cv2" not in sys.modules:
    sys.modules["cv2"] = _mock_cv2_module

# Modules that import get_db_connection directly
_DB_CLIENTS = [
    "database",
    "routers.admin",
    "routers.auth",
    "routers.history",
    "routers.inference",
    "routers.queue",
    "routers.trainer",
    "services.trainer_engine",
    "services.auth_service",
]


@pytest.fixture
def mock_db_connection():
    """Mock get_db_connection across all modules that import it directly."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_cursor.__iter__.return_value = iter([])
    mock_conn.cursor.return_value = mock_cursor
    patchers = [patch(f"{mod}.get_db_connection", return_value=mock_conn) for mod in _DB_CLIENTS]
    for p in patchers:
        p.start()
    yield {"conn": mock_conn, "cursor": mock_cursor}
    for p in patchers:
        p.stop()


@pytest.fixture
def client():
    tc = TestClient(app)
    # Pre-fetch CSRF token so the cookie is in the jar
    tc.get("/register")
    csrf = tc.cookies.get("csrf_token")
    if not csrf:
        csrf = secrets.token_urlsafe(32)
        tc.cookies.set("csrf_token", csrf)

    def _add_csrf(method):
        original = getattr(tc, method)
        def _wrapper(*args, **kwargs):
            headers = kwargs.pop("headers", {})
            if "X-CSRF-Token" not in headers:
                headers["X-CSRF-Token"] = csrf
            kwargs["headers"] = headers
            return original(*args, **kwargs)
        _wrapper.__name__ = method
        return _wrapper

    tc.post = _add_csrf("post")
    tc.put = _add_csrf("put")
    tc.delete = _add_csrf("delete")
    return tc


@pytest.fixture
def raw_client():
    """Client WITHOUT auto-CSRF handling. Used for CSRF-specific tests."""
    return TestClient(app)


@pytest.fixture
def auth_client(client, mock_db_connection):
    """Client with a valid JWT access token and a DB mock returning valid user."""
    cursor = mock_db_connection["cursor"]
    def fetchone_side_effect(*args, **kwargs):
        return {"id": 1, "username": "doctor1",
                "first_name": "Ana", "last_name": "Perez",
                "role": "Radiólogo Especialista"}
    cursor.fetchone.side_effect = fetchone_side_effect
    token = create_access_token(1)
    client.cookies.set("access_token", token)
    return client


@pytest.fixture
def mock_tf_model():
    """Mock a TF/Keras model with controlled predict output."""
    model = MagicMock()
    model.predict.return_value = [[0.85]]
    mock_logits = MagicMock()
    mock_logits.__getitem__.return_value = [0.85]
    mock_call_output = MagicMock()
    mock_call_output.logits = mock_logits
    model.__call__ = MagicMock(return_value=mock_call_output)
    return model


@pytest.fixture
def mock_ml_engine(mock_tf_model):
    """Mock ml_engine.get_model and process_and_predict at the consumer level."""
    with patch("services.ml_engine.get_model", return_value=mock_tf_model), \
         patch("routers.inference.process_and_predict", return_value=("Neumonía", 85.0)):
        yield


@pytest.fixture
def mock_xai_generator():
    """Mock xai_generator.generate_xai_heatmap at the consumer level."""
    with patch("routers.inference.generate_xai_heatmap", return_value="static/results/test_xai.png"):
        yield


@pytest.fixture
def mock_pdf_generator():
    """Mock pdf_generator.generate_medical_report at the consumer level."""
    with patch("routers.inference.generate_medical_report", return_value="static/reports/test_report.pdf"):
        yield
