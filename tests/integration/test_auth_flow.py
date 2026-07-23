class TestAuthFlow:
    def test_register_login_dashboard(self, client, sqlite_db):
        # Register
        resp = client.post("/api/register", data={
            "username": "doctor1", "password": "pass",
            "first_name": "Ana", "last_name": "Perez",
            "role": "Radiólogo Especialista"
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"
        token = resp.cookies.get("session_token")
        assert token is not None

        # Dashboard with token
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "Ana" in resp.text

    def test_login_with_registered_user(self, client, sqlite_db):
        # Seed user directly
        cur = sqlite_db.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, first_name, last_name, role) "
            "VALUES (?, ?, ?, ?, ?)",
            ("existing", "secret", "Carlos", "Lopez", "Neumólogo")
        )
        sqlite_db.commit()

        # Login
        resp = client.post("/login", data={"username": "existing", "password": "secret"},
                           follow_redirects=False)
        assert resp.status_code == 303
        assert resp.headers["location"] == "/dashboard"

        # Follow redirect
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "Carlos" in resp.text

    def test_dashboard_without_login_redirects(self, client):
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code == 303
        assert resp.headers["location"] == "/"

    def test_history_empty_for_new_user(self, client, sqlite_db):
        cur = sqlite_db.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, first_name, last_name, role) "
            "VALUES (?, ?, ?, ?, ?)",
            ("newdoc", "x", "Nuevo", "Doctor", "Residente")
        )
        sqlite_db.commit()
        client.cookies.set("session_token", "1")
        resp = client.get("/api/history")
        assert resp.status_code == 200
        assert resp.json()["data"] == []
