import re

from fastapi import APIRouter, Cookie, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import get_db_connection
from services.auth_service import (
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
    hash_password,
    revoke_refresh_token,
    rotate_refresh_token,
    verify_password,
    verify_refresh_token,
)
from services.rate_limiter import limiter

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_register_inputs(username: str, password: str, first_name: str, last_name: str) -> str | None:
    cleaned = username.strip()
    if not cleaned or not _EMAIL_RE.match(cleaned):
        return "username"
    if len(password) < 8:
        return "password"
    if not first_name.strip():
        return "first_name"
    if not last_name.strip():
        return "last_name"
    return None


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 1. PANTALLA DE INICIO (LOGIN)
@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

# 2. PROCESAR EL LOGIN
@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user["password_hash"]):
        response = RedirectResponse(url="/dashboard", status_code=303)
        access_token = create_access_token(user["id"])
        refresh_token = create_refresh_token(user["id"])
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax", path="/api/token/refresh")
        return response
    else:
        return RedirectResponse(url="/?error=1", status_code=303)

# 3. PANTALLA PRINCIPAL (DASHBOARD)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name, last_name, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return RedirectResponse(url="/logout", status_code=303)

    fname = user.get('first_name') or "Usuario"
    lname = user.get('last_name') or ""
    full_name = f"{fname} {lname}".strip()
    role = user.get('role') or "Facultativo"

    response = templates.TemplateResponse("dashboard.html", {
        "request": request,
        "full_name": full_name,
        "role": role
    })

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# 4. PANTALLA DE ENTRENAMIENTO (MLOps)
@router.get("/training", response_class=HTMLResponse)
async def training_lab(request: Request):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return RedirectResponse(url="/", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name, last_name, role FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return RedirectResponse(url="/logout", status_code=303)

    fname = user.get('first_name') or "Usuario"
    lname = user.get('last_name') or ""
    full_name = f"{fname} {lname}".strip()
    role = user.get('role') or "Facultativo"

    response = templates.TemplateResponse("training.html", {
        "request": request,
        "full_name": full_name,
        "role": role
    })

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# 5. REFRESCAR TOKEN
@router.post("/api/token/refresh")
async def token_refresh(refresh_token: str = Cookie(None)):
    if not refresh_token:
        return JSONResponse(status_code=401, content={"status": "error", "message": "No refresh token"})
    new_raw_refresh = rotate_refresh_token(refresh_token)
    if not new_raw_refresh:
        return JSONResponse(status_code=401, content={"status": "error", "message": "Invalid or revoked refresh token"})
    user_id = verify_refresh_token(new_raw_refresh)
    if not user_id:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Error al procesar el refresh token"})
    access = create_access_token(user_id)
    response = JSONResponse(content={"status": "success"})
    response.set_cookie(key="access_token", value=access, httponly=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=new_raw_refresh, httponly=True, samesite="lax", path="/api/token/refresh")
    return response

# 6. CERRAR SESIÓN
@router.get("/logout")
async def logout(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        revoke_refresh_token(refresh_token)
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/api/token/refresh")
    return response

# 6. PANTALLA DE REGISTRO
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 7. PROCESAR EL REGISTRO
@router.post("/api/register")
async def process_register(
    username: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    role: str = Form(...)
):
    try:
        invalid_field = _validate_register_inputs(username, password, first_name, last_name)
        if invalid_field:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "code": "validation_error", "field": invalid_field}
            )

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return JSONResponse(status_code=400, content={"status": "error", "code": "user_exists"})

        query = """
        INSERT INTO users (username, password_hash, first_name, last_name, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, hash_password(password), first_name, last_name, role))
        conn.commit()

        new_user_id = cursor.lastrowid
        conn.close()

        response = JSONResponse(content={"status": "success", "code": "success_register"})
        access_token = create_access_token(new_user_id)
        refresh_token = create_refresh_token(new_user_id)
        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax", path="/api/token/refresh")
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "code": "server_error", "details": str(e)})
