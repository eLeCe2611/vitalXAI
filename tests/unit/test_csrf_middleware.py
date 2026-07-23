class TestCsrfMiddleware:
    def test_get_response_includes_csrf_cookie(self, raw_client):
        response = raw_client.get("/")
        assert "csrf_token" in response.cookies
        assert len(response.cookies["csrf_token"]) > 16

    def test_post_without_csrf_token_returns_403(self, raw_client, mock_db_connection):
        response = raw_client.post("/api/register", data={
            "username": "test", "password": "pass",
            "first_name": "T", "last_name": "U", "role": "Doc"
        })
        assert response.status_code == 403

    def test_post_with_matching_csrf_token_succeeds(self, raw_client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2

        response = raw_client.get("/register")
        csrf_token = response.cookies["csrf_token"]

        response = raw_client.post("/api/register", data={
            "username": "newdoctor@hospital.com", "password": "pass1234",
            "first_name": "New", "last_name": "Doc", "role": "Médico Residente"
        }, headers={"X-CSRF-Token": csrf_token})
        assert response.status_code == 200

    def test_get_methods_are_exempt_from_csrf(self, raw_client):
        response = raw_client.get("/register")
        assert response.status_code == 200

    def test_post_with_wrong_csrf_token_returns_403(self, raw_client, mock_db_connection):
        raw_client.get("/")
        response = raw_client.post("/api/register", data={
            "username": "test", "password": "pass",
            "first_name": "T", "last_name": "U", "role": "Doc"
        }, headers={"X-CSRF-Token": "wrong-token-value"})
        assert response.status_code == 403
