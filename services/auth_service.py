import datetime
import hashlib
import os
import secrets

import bcrypt
from jose import jwt

from database import get_db_connection

JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production")
JWT_ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", "15"))
JWT_REFRESH_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))
# Grace period in seconds for refresh token rotation (allows concurrent requests)
REFRESH_ROTATION_GRACE_SECONDS = int(os.getenv("REFRESH_ROTATION_GRACE_SECONDS", "60"))

if JWT_SECRET_KEY == "dev-secret-change-in-production":  # noqa: S105
    import warnings
    warnings.warn(
        "JWT_SECRET_KEY no configurada. Usando clave por defecto insegura. "
        "Configura JWT_SECRET_KEY en .env para producción.",
        stacklevel=2,
    )


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except (ValueError, TypeError):
        return False


# --- JWT Helpers ---

def get_user_id_from_token(token: str | None) -> int | None:
    """Extract user_id from an access token string (None if missing or invalid)."""
    if not token:
        return None
    return verify_access_token(token)


# --- JWT Access Tokens ---

def create_access_token(user_id: int) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
        return int(sub) if sub is not None else None
    except Exception:
        return None


# --- Refresh Tokens (stored in DB) ---

def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def create_refresh_token(user_id: int) -> str:
    raw_token = secrets.token_urlsafe(48)
    token_hash = _hash_token(raw_token)
    expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO refresh_tokens (user_id, token_hash, expires_at) VALUES (%s, %s, %s)",
        (user_id, token_hash, expires_at)
    )
    conn.commit()
    conn.close()
    return raw_token


def verify_refresh_token(raw_token: str) -> int | None:
    token_hash = _hash_token(raw_token)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Active (non-revoked) token — normal case
    cursor.execute(
        "SELECT user_id FROM refresh_tokens WHERE token_hash = %s AND revoked = FALSE AND expires_at > NOW()",
        (token_hash,)
    )
    row = cursor.fetchone()
    if row:
        conn.close()
        return row["user_id"]

    # 2. Recently revoked token (within grace period) — concurrent rotation
    cursor.execute(
        "SELECT user_id FROM refresh_tokens WHERE token_hash = %s "
        "AND revoked = TRUE AND expires_at > NOW() "
        "AND created_at > NOW() - INTERVAL %s SECOND",
        (token_hash, REFRESH_ROTATION_GRACE_SECONDS),
    )
    row = cursor.fetchone()
    if row:
        conn.close()
        return row["user_id"]

    # 3. Old revoked token (outside grace period) → theft detected
    cursor.execute(
        "SELECT user_id FROM refresh_tokens WHERE token_hash = %s AND revoked = TRUE",
        (token_hash,)
    )
    row = cursor.fetchone()
    if row:
        user_id = row["user_id"]
        # Revoke ALL tokens for this user (theft detection)
        cursor.execute("UPDATE refresh_tokens SET revoked = TRUE WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()
        return None

    conn.close()
    return None


def revoke_refresh_token(raw_token: str) -> None:
    token_hash = _hash_token(raw_token)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE refresh_tokens SET revoked = TRUE WHERE token_hash = %s", (token_hash,))
    conn.commit()
    conn.close()


def rotate_refresh_token(old_raw_token: str) -> str | None:
    user_id = verify_refresh_token(old_raw_token)
    if user_id is None:
        return None
    revoke_refresh_token(old_raw_token)
    return create_refresh_token(user_id)
