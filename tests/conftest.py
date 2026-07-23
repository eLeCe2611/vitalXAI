from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app

# Modules that import get_db_connection directly
_DB_CLIENTS = [
    "database",
    "routers.auth",
    "routers.history",
    "routers.inference",
    "services.trainer_engine",
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
    return TestClient(app)


@pytest.fixture
def auth_client(client, mock_db_connection):
    """Client with a valid session cookie and a DB mock returning valid user."""
    cursor = mock_db_connection["cursor"]
    def fetchone_side_effect(*args, **kwargs):
        return {"id": 1, "username": "doctor1",
                "first_name": "Ana", "last_name": "Perez",
                "role": "Radiólogo Especialista"}
    cursor.fetchone.side_effect = fetchone_side_effect
    client.cookies.set("session_token", "1")
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
