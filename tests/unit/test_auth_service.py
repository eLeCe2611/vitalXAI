
from jose import jwt


class TestJwtTokens:
    def test_create_access_token_returns_token(self):
        from services.auth_service import create_access_token
        token = create_access_token(42)
        payload = jwt.decode(token, "dev-secret-change-in-production", algorithms=["HS256"])
        assert payload["sub"] == "42"
        assert "exp" in payload

    def test_verify_access_token_returns_user_id(self):
        from services.auth_service import create_access_token, verify_access_token
        token = create_access_token(7)
        user_id = verify_access_token(token)
        assert user_id == 7

    def test_verify_access_token_returns_none_for_expired(self):
        import datetime

        from jose import jwt

        from services.auth_service import verify_access_token
        expired_token = jwt.encode(
            {"sub": 1, "exp": datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=1)},
            "dev-secret-change-in-production", algorithm="HS256"
        )
        assert verify_access_token(expired_token) is None

    def test_verify_access_token_returns_none_for_invalid(self):
        from services.auth_service import verify_access_token
        assert verify_access_token("invalid-token") is None

    def test_create_refresh_token_stores_in_db(self):
        from unittest.mock import MagicMock
        from unittest.mock import patch as p

        from services.auth_service import create_refresh_token
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        with p("services.auth_service.get_db_connection", return_value=mock_conn):
            raw_token = create_refresh_token(42)
        assert raw_token is not None
        assert mock_cursor.execute.called
        call_args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO refresh_tokens" in call_args[0]

    def test_verify_refresh_token_returns_user_id(self):
        from unittest.mock import MagicMock
        from unittest.mock import patch as p

        from services.auth_service import create_refresh_token, verify_refresh_token
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        with p("services.auth_service.get_db_connection", return_value=mock_conn):
            raw_token = create_refresh_token(42)
            mock_cursor.fetchone.return_value = {"user_id": 42}
            user_id = verify_refresh_token(raw_token)
        assert user_id == 42

    def test_rotate_refresh_token_invalidates_old(self):
        from unittest.mock import MagicMock
        from unittest.mock import patch as p

        from services.auth_service import create_refresh_token, rotate_refresh_token
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        with p("services.auth_service.get_db_connection", return_value=mock_conn):
            old_token = create_refresh_token(42)
            mock_cursor.fetchone.return_value = {"user_id": 42}
            new_token = rotate_refresh_token(old_token)
        assert new_token is not None
        assert new_token != old_token

    def test_revoked_refresh_token_returns_none(self):
        from unittest.mock import MagicMock
        from unittest.mock import patch as p

        from services.auth_service import verify_refresh_token
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        with p("services.auth_service.get_db_connection", return_value=mock_conn):
            result = verify_refresh_token("any-token")
        assert result is None

    def test_grace_period_accepts_recently_revoked_token(self):
        """Verify that a recently revoked token is still accepted within grace period."""
        from unittest.mock import MagicMock
        from unittest.mock import patch as p

        from services.auth_service import verify_refresh_token
        mock_cursor = MagicMock()
        # First query (active token): returns None
        # Second query (grace period): returns user_id
        mock_cursor.fetchone.side_effect = [None, {"user_id": 42}]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        with p("services.auth_service.get_db_connection", return_value=mock_conn):
            result = verify_refresh_token("recently-revoked-token")
        assert result == 42
