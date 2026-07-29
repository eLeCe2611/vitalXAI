class TestRateLimiting:
    def test_login_limited_to_5_per_minute(self, raw_client, mock_db_connection):
        """Login endpoint should return 429 after 5 rapid attempts."""
        storage = raw_client.app.state.limiter._limiter.storage
        storage.reset()

        raw_client.get("/register")
        for i in range(5):
            r = raw_client.post(
                "/login", data={"username": "x", "password": "x"},
                headers={"X-CSRF-Token": raw_client.cookies.get("csrf_token", "")},
                follow_redirects=False
            )
            assert r.status_code == 303, f"Attempt {i+1} got {r.status_code}"
        r = raw_client.post(
            "/login", data={"username": "x", "password": "x"},
            headers={"X-CSRF-Token": raw_client.cookies.get("csrf_token", "")},
            follow_redirects=False
        )
        assert r.status_code == 429

    def test_default_limit_allows_normal_requests(self, raw_client):
        """Non-login endpoints should have a higher default limit."""
        storage = raw_client.app.state.limiter._limiter.storage
        storage.reset()

        for _ in range(30):
            r = raw_client.get("/")
            assert r.status_code == 200
