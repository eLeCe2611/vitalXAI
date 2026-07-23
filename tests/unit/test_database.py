from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_mysql_connector():
    with patch("database.mysql.connector") as mock:
        yield mock


class TestGetDbConnection:
    def test_uses_defaults_when_no_env(self, mock_mysql_connector):
        """Should fall back to localhost defaults when env vars are not set."""
        from database import get_db_connection
        mock_mysql_connector.connect.return_value = "fake_conn"
        result = get_db_connection()
        assert result == "fake_conn"
        mock_mysql_connector.connect.assert_called_once_with(
            host="localhost", user="root", password="", database="tfg_pneumonia"
        )

    def test_reads_credentials_from_env(self, mock_mysql_connector):
        """Should read DB credentials from environment variables when set."""
        import os
        from unittest.mock import patch

        with patch.dict(os.environ, {
            "DB_HOST": "env-host",
            "DB_USER": "env-user",
            "DB_PASSWORD": "env-pass",
            "DB_NAME": "env-db"
        }):
            from database import get_db_connection
            mock_mysql_connector.connect.return_value = "fake_conn_env"
            result = get_db_connection()
            assert result == "fake_conn_env"
            mock_mysql_connector.connect.assert_called_once_with(
                host="env-host", user="env-user", password="env-pass", database="env-db"  # noqa: S106
            )

    def test_raises_on_connection_error(self, mock_mysql_connector):
        from database import get_db_connection
        mock_mysql_connector.connect.side_effect = Exception("Connection refused")
        with pytest.raises(Exception, match="Connection refused"):
            get_db_connection()


class TestInitDb:
    def test_creates_training_jobs_table(self, mock_mysql_connector):
        from database import init_db
        mock_conn = MagicMock()
        mock_mysql_connector.connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        init_db()
        assert mock_cursor.execute.call_count == 2
        call_sql = mock_cursor.execute.call_args_list[0][0][0]
        assert "CREATE TABLE IF NOT EXISTS training_jobs" in call_sql
        call_sql2 = mock_cursor.execute.call_args_list[1][0][0]
        assert "CREATE TABLE IF NOT EXISTS refresh_tokens" in call_sql2
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_handles_db_not_available(self, mock_mysql_connector):
        from database import init_db
        mock_mysql_connector.connect.side_effect = Exception("MySQL not running")
        with pytest.raises(Exception, match="MySQL not running"):
            init_db()
