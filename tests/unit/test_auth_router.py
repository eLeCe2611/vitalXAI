

class TestLoginPage:
    def test_returns_login_form(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestLogin:
    def test_valid_credentials_redirects_to_dashboard(self, client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"id": 1}
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
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {
            "first_name": "Ana", "last_name": "Perez", "role": "Radiólogo Especialista"
        }
        client.cookies.set("session_token", "1")
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "Ana" in response.text

    def test_redirects_to_logout_for_invalid_user(self, client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = None
        client.cookies.set("session_token", "999")
        response = client.get("/dashboard", follow_redirects=False)
        assert response.status_code == 303
        assert "logout" in response.headers["location"]


class TestTraining:
    def test_requires_authentication(self, client):
        response = client.get("/training", follow_redirects=False)
        assert response.status_code == 303

    def test_shows_page_when_authenticated(self, mock_db_connection, client):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {
            "first_name": "Ana", "last_name": "Perez", "role": "Radiólogo Especialista"
        }
        client.cookies.set("session_token", "1")
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
            "username": "newdoctor", "password": "pass",
            "first_name": "New", "last_name": "Doc", "role": "Médico Residente"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_duplicate_username_returns_error(self, mock_db_connection, client):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = {"id": 1}
        response = client.post("/api/register", data={
            "username": "existing", "password": "pass",
            "first_name": "Old", "last_name": "User", "role": "Neumólogo"
        })
        assert response.status_code == 400
        assert response.json()["code"] == "user_exists"
