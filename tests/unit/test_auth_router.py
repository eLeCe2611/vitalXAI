

class TestLoginPage:
    def test_returns_login_form(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestLogin:
    def test_valid_credentials_redirects_to_dashboard(self, client, mock_db_connection):
        import bcrypt as _bcrypt
        cursor = mock_db_connection["cursor"]
        hash_value = _bcrypt.hashpw(b"pass123", _bcrypt.gensalt()).decode()
        cursor.fetchone.return_value = {"id": 1, "password_hash": hash_value}
        response = client.post("/login", data={"username": "doctor1", "password": "pass123"},
                               follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/dashboard"

    def test_invalid_credentials_shows_error(self, client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = None
        response = client.post("/login", data={"username": "bad", "password": "wrong"},
                               follow_redirects=False)
        assert response.status_code == 303
        assert "error=1" in response.headers["location"]


class TestDashboard:
    def test_requires_authentication(self, client):
        response = client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/"

    def test_shows_user_info_when_authenticated(self, mock_db_connection, client):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {
            "first_name": "Ana", "last_name": "Perez", "role": "Radiólogo Especialista"
        }
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "Ana" in response.text

    def test_redirects_to_logout_for_invalid_user(self, client, mock_db_connection):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = None
        token = create_access_token(999)
        client.cookies.set("access_token", token)
        response = client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 303
        assert "logout" in response.headers["location"]


class TestTraining:
    def test_requires_authentication(self, client):
        response = client.get("/training", follow_redirects=False)
        assert response.status_code == 303

    def test_shows_page_when_authenticated(self, mock_db_connection, client):
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {
            "first_name": "Ana", "last_name": "Perez", "role": "Radiólogo Especialista"
        }
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.get("/training")
        assert response.status_code == 200


class TestLogout:
    def test_clears_session_cookie(self, client):
        response = client.get("/logout", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/"


class TestRegisterPage:
    def test_returns_register_form(self, client):
        response = client.get("/register")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestProcessRegister:
    def test_successful_registration(self, mock_db_connection, client):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2
        response = client.post("/api/register", data={
            "username": "newdoctor@hospital.com", "password": "pass1234",
            "first_name": "New", "last_name": "Doc", "role": "Médico Residente"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_registration_stores_bcrypt_hash(self, mock_db_connection, client):
        """Password must be stored as bcrypt hash, not plaintext."""
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2
        client.post("/api/register", data={
            "username": "newdoctor@hospital.com", "password": "securepass123",
            "first_name": "New", "last_name": "Doc", "role": "Médico Residente"
        })
        insert_call = cursor.execute.call_args_list[1]
        insert_params = insert_call[0][1]
        stored_password = insert_params[1]
        assert stored_password.startswith("$2b$"), "Password should be a bcrypt hash"

    def test_duplicate_username_returns_error(self, mock_db_connection, client):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"id": 1}
        response = client.post("/api/register", data={
            "username": "existing@doctor.com", "password": "pass1234",
            "first_name": "Old", "last_name": "User", "role": "Neumólogo"
        })
        assert response.status_code == 400
        assert response.json()["code"] == "user_exists"


class TestBcryptLogin:
    """Tests for bcrypt-based login verification."""

    def test_login_verifies_password_against_hash(self, client):
        """Login should verify password against stored bcrypt hash."""
        from unittest.mock import MagicMock, patch

        import bcrypt as _bcrypt

        mock_cursor = MagicMock()
        hash_value = _bcrypt.hashpw(b"correct_password", _bcrypt.gensalt()).decode()
        mock_cursor.fetchone.return_value = {"id": 1, "password_hash": hash_value}
        mock_cursor.lastrowid = 1
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("routers.auth.get_db_connection", return_value=mock_conn), \
             patch("services.auth_service.get_db_connection", return_value=mock_conn):
            response = client.post("/login", data={"username": "doctor1", "password": "correct_password"},
                                   follow_redirects=False)
            assert response.status_code == 303
            assert response.headers["location"] == "/dashboard"

    def test_login_wrong_password_returns_error(self, client):
        """Login with wrong password should fail after bcrypt refactor."""
        from unittest.mock import MagicMock, patch

        import bcrypt as _bcrypt

        mock_cursor = MagicMock()
        hash_value = _bcrypt.hashpw(b"correct_password", _bcrypt.gensalt()).decode()
        mock_cursor.fetchone.return_value = {"id": 1, "password_hash": hash_value}
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("routers.auth.get_db_connection", return_value=mock_conn):
            response = client.post("/login", data={"username": "doctor1", "password": "wrong_password"},
                                   follow_redirects=False)
            assert response.status_code == 303
            assert "error=1" in response.headers["location"]
