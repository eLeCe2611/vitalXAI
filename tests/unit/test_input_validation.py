import io


class TestRegisterValidation:
    def test_rejects_invalid_email_format(self, client, mock_db_connection):
        """Register should reject invalid email format in username."""
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2
        response = client.post("/api/register", data={
            "username": "not-an-email", "password": "pass123",
            "first_name": "Test", "last_name": "User", "role": "Doc"
        })
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "validation_error"
        assert data["field"] == "username"

    def test_rejects_empty_username(self, raw_client, mock_db_connection):
        """Empty username should be rejected by FastAPI's 'missing' validation."""
        raw_client.get("/register")
        csrf = raw_client.cookies.get("csrf_token", "")
        response = raw_client.post("/api/register", data={
            "username": "", "password": "pass123",
            "first_name": "Test", "last_name": "User", "role": "Doc"
        }, headers={"X-CSRF-Token": csrf})
        assert response.status_code == 422

    def test_accepts_valid_email(self, client, mock_db_connection):
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2
        response = client.post("/api/register", data={
            "username": "doctor@hospital.com", "password": "pass1234",
            "first_name": "Test", "last_name": "User", "role": "Doc"
        })
        assert response.status_code == 200

    def test_rejects_empty_first_name(self, raw_client, mock_db_connection):
        """Empty first_name is caught by FastAPI validation."""
        raw_client.get("/register")
        csrf = raw_client.cookies.get("csrf_token", "")
        response = raw_client.post("/api/register", data={
            "username": "doc@h.com", "password": "pass123",
            "first_name": "", "last_name": "User", "role": "Doc"
        }, headers={"X-CSRF-Token": csrf})
        assert response.status_code == 422

    def test_rejects_short_password(self, raw_client, mock_db_connection):
        """Register should reject passwords shorter than 8 characters."""
        raw_client.get("/register")
        csrf = raw_client.cookies.get("csrf_token", "")
        response = raw_client.post("/api/register", data={
            "username": "doc@h.com", "password": "short",
            "first_name": "Test", "last_name": "User", "role": "Doc"
        }, headers={"X-CSRF-Token": csrf})
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "validation_error"
        assert data["field"] == "password"

    def test_accepts_password_with_min_length(self, raw_client, mock_db_connection):
        """Register should accept passwords with 8 or more characters."""
        raw_client.get("/register")
        csrf = raw_client.cookies.get("csrf_token", "")
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.side_effect = [None, None]
        cursor.lastrowid = 2
        response = raw_client.post("/api/register", data={
            "username": "doc@h.com", "password": "pass1234",
            "first_name": "Test", "last_name": "User", "role": "Doc"
        }, headers={"X-CSRF-Token": csrf})
        assert response.status_code == 200


class TestFileValidation:
    def test_rejects_oversized_file(self, client, mock_db_connection):
        """Predict should reject files larger than 10MB."""
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = [0]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        large_data = b"x" * (11 * 1024 * 1024)
        response = client.post("/predict", data={"model_name": "DenseNet121"},
                               files={"file": ("big.jpg", io.BytesIO(large_data), "image/jpeg")})
        assert response.status_code == 400

    def test_rejects_non_image_file(self, client, mock_db_connection):
        """Predict should reject non-image file types."""
        from services.auth_service import create_access_token
        cursor = mock_db_connection["cursor"]
        cursor.fetchone.return_value = [0]
        token = create_access_token(1)
        client.cookies.set("access_token", token)
        response = client.post("/predict", data={"model_name": "DenseNet121"},
                               files={"file": ("doc.pdf", io.BytesIO(b"%PDF-"), "application/pdf")})
        assert response.status_code == 400
