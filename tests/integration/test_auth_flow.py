class TestAuthFlow:
    def test_register_login_dashboard(self, client, sqlite_db):
        # Register
        resp = client.post("/api/register", data={
            "username": "doctor1@hospital.com", "password": "pass1234",
            "first_name": "Ana", "last_name": "Perez",
            "role": "Radiólogo Especialista"
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"
        token = resp.cookies.get("access_token")
        assert token is not None

        # Dashboard with token
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "Ana" in resp.text

    def test_login_with_registered_user(self, client, sqlite_db):
        import bcrypt as _bcrypt
        # Seed user directly with bcrypt hash
        cur = sqlite_db.cursor()
        hashed = _bcrypt.hashpw(b"secret", _bcrypt.gensalt()).decode()
        cur.execute(
            "INSERT INTO users (username, password_hash, first_name, last_name, role) "
            "VALUES (?, ?, ?, ?, ?)",
            ("existing@hospital.com", hashed, "Carlos", "Lopez", "Neumólogo")
        )
        sqlite_db.commit()

        # Login
        resp = client.post("/login", data={"username": "existing@hospital.com", "password": "secret"},
                           follow_redirects=False)
        assert resp.status_code == 303
        assert resp.headers["location"] == "/dashboard"

        # Follow redirect (now with JWT cookies from login)
        resp = client.get("/dashboard")
        assert resp.status_code == 200
        assert "Carlos" in resp.text

    def test_dashboard_without_login_redirects(self, client):
        resp = client.get("/dashboard", follow_redirects=False)
        assert resp.status_code == 303
        assert resp.headers["location"] == "/"

    def test_history_empty_for_new_user(self, client, sqlite_db):
        from services.auth_service import create_access_token
        cur = sqlite_db.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, first_name, last_name, role) "
            "VALUES (?, ?, ?, ?, ?)",
            ("newdoc", "x", "Nuevo", "Doctor", "Residente")
        )
        sqlite_db.commit()
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        resp = client.get("/api/history")
        assert resp.status_code == 200
        assert resp.json()["data"] == []
