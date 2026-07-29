class TestSecurityHeaders:
    def test_x_content_type_options(self, client):
        response = client.get("/")
        assert response.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options(self, client):
        response = client.get("/")
        assert response.headers.get("x-frame-options") == "DENY"

    def test_strict_transport_security(self, client):
        response = client.get("/")
        assert response.headers.get("strict-transport-security") == "max-age=31536000; includeSubDomains"

    def test_x_xss_protection(self, client):
        response = client.get("/")
        assert response.headers.get("x-xss-protection") == "1; mode=block"

    def test_referrer_policy(self, client):
        response = client.get("/")
        assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

    def test_content_security_policy(self, client):
        response = client.get("/")
        csp = response.headers.get("content-security-policy")
        assert csp is not None
        assert "default-src 'self'" in csp

    def test_headers_on_all_responses(self, client):
        response = client.get("/register")
        assert response.headers.get("x-content-type-options") == "nosniff"
