from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def reset_pool():
    import database
    database._pool = None


@pytest.fixture(autouse=True)
def mock_db_pool():
    """Mock MySQLConnectionPool to avoid real MySQL connections."""
    with patch("database.MySQLConnectionPool") as mock:
        yield mock


class TestGetDbConnection:
    def test_uses_defaults_when_no_env(self, mock_db_pool):
        """Should fall back to localhost defaults when env vars are not set."""
        from database import get_db_connection
        mock_conn = MagicMock()
        mock_db_pool.return_value.get_connection.return_value = mock_conn
        result = get_db_connection()
        assert result == mock_conn
        _, kwargs = mock_db_pool.call_args
        assert kwargs["host"] == "localhost"
        assert kwargs["user"] == "root"
        assert kwargs["password"] == ""
        assert kwargs["database"] == "tfg_pneumonia"
        assert kwargs["pool_name"] == "mypool"
        assert kwargs["pool_size"] == 5

    def test_reads_credentials_from_env(self, mock_db_pool):
        """Should read DB credentials from environment variables when set."""
        import os
        from unittest.mock import patch as p

        with p.dict(os.environ, {
            "DB_HOST": "env-host",
            "DB_USER": "env-user",
            "DB_PASSWORD": "env-pass",
            "DB_NAME": "env-db",
            "DB_POOL_SIZE": "10"
        }):
            from database import get_db_connection
            mock_conn = MagicMock()
            mock_db_pool.return_value.get_connection.return_value = mock_conn
            result = get_db_connection()
            assert result == mock_conn
            _, kwargs = mock_db_pool.call_args
            assert kwargs["host"] == "env-host"
            assert kwargs["user"] == "env-user"
            assert kwargs["password"] == "env-pass"  # noqa: S105
            assert kwargs["database"] == "env-db"
            assert kwargs["pool_size"] == 10

    def test_pool_is_reused(self, mock_db_pool):
        """The pool should be created once and reused."""
        from database import get_db_connection
        mock_conn = MagicMock()
        mock_db_pool.return_value.get_connection.return_value = mock_conn
        get_db_connection()
        get_db_connection()
        assert mock_db_pool.call_count == 1

    def test_raises_on_connection_error(self, mock_db_pool):
        from database import get_db_connection
        mock_db_pool.return_value.get_connection.side_effect = Exception("Connection refused")
        with pytest.raises(Exception, match="Connection refused"):
            get_db_connection()


class TestInitDb:
    def test_creates_all_tables(self, mock_db_pool):
        from database import init_db
        mock_conn = MagicMock()
        mock_db_pool.return_value.get_connection.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        init_db()
        assert mock_cursor.execute.call_count == 4
        tables = ["users", "consultations", "training_jobs", "refresh_tokens"]
        for i, table in enumerate(tables):
            sql = mock_cursor.execute.call_args_list[i][0][0]
            assert f"CREATE TABLE IF NOT EXISTS {table}" in sql
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_handles_db_not_available(self, mock_db_pool):
        from database import init_db
        mock_db_pool.return_value.get_connection.side_effect = Exception("MySQL not running")
        with pytest.raises(Exception, match="MySQL not running"):
            init_db()
