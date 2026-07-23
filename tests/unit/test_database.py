from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_mysql_connector():
    with patch("database.mysql.connector") as mock:
        yield mock


class TestGetDbConnection:
    def test_returns_connection(self, mock_mysql_connector):
        from database import get_db_connection
        mock_mysql_connector.connect.return_value = "fake_conn"
        result = get_db_connection()
        assert result == "fake_conn"
        mock_mysql_connector.connect.assert_called_once_with(
            host="localhost", user="root", password="", database="tfg_pneumonia"
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
        mock_cursor.execute.assert_called_once()
        call_sql = mock_cursor.execute.call_args[0][0]
        assert "CREATE TABLE IF NOT EXISTS training_jobs" in call_sql
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_handles_db_not_available(self, mock_mysql_connector):
        from database import init_db
        mock_mysql_connector.connect.side_effect = Exception("MySQL not running")
        with pytest.raises(Exception, match="MySQL not running"):
            init_db()
