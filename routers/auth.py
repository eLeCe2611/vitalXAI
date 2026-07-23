from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import get_db_connection

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 1. PANTALLA DE INICIO (LOGIN)
@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

# 2. PROCESAR EL LOGIN
@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s AND password_hash = %s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="session_token", value=str(user["id"]))
        return response
    else:
        return RedirectResponse(url="/?error=1", status_code=303)

# 3. PANTALLA PRINCIPAL (DASHBOARD)
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    session_token = request.cookies.get("session_token")
    if not session_token:
        return RedirectResponse(url="/", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name, last_name, role FROM users WHERE id = %s", (session_token,))
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
    session_token = request.cookies.get("session_token")
    if not session_token:
        return RedirectResponse(url="/", status_code=303)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT first_name, last_name, role FROM users WHERE id = %s", (session_token,))
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

# 5. CERRAR SESIÓN
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_token")
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
        cursor.execute(query, (username, password, first_name, last_name, role))
        conn.commit()

        new_user_id = cursor.lastrowid
        conn.close()

        response = JSONResponse(content={"status": "success", "code": "success_register"})
        response.set_cookie(key="session_token", value=str(new_user_id))
        return response

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "code": "server_error", "details": str(e)})
