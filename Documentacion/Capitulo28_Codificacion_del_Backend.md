# Capítulo 28: Codificación del backend

El backend de vitalXAI materializa las capas de la aplicación descritas en el capítulo 23: la capa HTTP, la capa de servicios, la persistencia relacional y los mecanismos de seguridad transversales. Este capítulo describe la codificación de estas capas, presentando los componentes implementados y los fragmentos de código más representativos de cada uno, con la explicación de las decisiones de implementación que los sustentan. La codificación del backend se organiza en cinco apartados: el arranque y la configuración de la aplicación, la capa HTTP de los routers, los servicios de aplicación, la persistencia y el acceso a los datos, y la seguridad transversal.

El backend se construye sobre FastAPI, servido por Uvicorn, y se apoya en MySQL para la persistencia (FastAPI, 2024; Uvicorn, 2024; Oracle, 2024). La implementación sigue el patrón de fachada ligera descrito en el diseño: los routers se ocupan de la recepción y la serialización de las peticiones HTTP, y delegan la lógica en los servicios, que concentran las operaciones de aplicación y acceden a la persistencia. Esta separación, ya declarada en el capítulo 17, se refleja en la estructura de los paquetes `routers/` y `services/` descrita en el capítulo 27, y permite verificar cada componente de forma aislada mediante las pruebas unitarias del capítulo 16.

## 28.1 Arranque y configuración de la aplicación

El punto de entrada de la aplicación se implementa en el módulo `main.py`, que compone la aplicación FastAPI, configura los mecanismos de seguridad transversales, monta los recursos estáticos e integra los routers de los subsistemas. El arranque se gestiona mediante el ciclo de vida de la aplicación: al iniciarse, se inicializa la base de datos y se arranca el worker de la cola; al finalizar, el worker queda detenido con la aplicación. El fragmento siguiente muestra la implementación del ciclo de vida y de la composición de la aplicación.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("Base de datos conectada e inicializada correctamente.")
    except Exception:
        print("ATENCIÓN: No se pudo conectar a la base de datos MySQL.")
    start_worker(app)
    print("Worker de cola iniciado.")
    yield

app = FastAPI(title="X-Ray AI Consultant", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CSRFMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("training_results", exist_ok=True)
app.mount("/training_results", StaticFiles(directory="training_results"), name="training_results")

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(inference.router)
app.include_router(queue.router)
app.include_router(trainer.router)
```

*Código 28.1 - Arranque y composición de la aplicación (`main.py`)*

La implementación del arranque refleja las decisiones del diseño. La inicialización de la base de datos se realiza mediante la función `init_db()` de `database.py`, que crea las tablas del esquema si no existen, de modo que el arranque no requiere un script de instalación previo; el fallo de conexión se captura y se informa sin interrumpir el arranque, en coherencia con el entorno de construcción del capítulo 23. El worker de la cola se arranca mediante `start_worker()`, que crea la tarea asíncrona del procesamiento en segundo plano. Los mecanismos de seguridad se añaden como middleware —las cabeceras de seguridad y la protección CSRF— y el limitador de peticiones se registra en el estado de la aplicación con su manejador de excepciones. Los recursos estáticos y el directorio de resultados de entrenamiento se montan como directorios servidos por la aplicación, y los routers de los seis subsistemas se integran mediante la inclusión de sus enrutadores.

## 28.2 Capa HTTP: los routers

La capa HTTP se implementa en el paquete `routers/`, con un módulo por subsistema: `auth.py` para el acceso y las sesiones, `inference.py` para el diagnóstico, `history.py` para el historial, `queue.py` para la cola de trabajos, `trainer.py` para el laboratorio MLOps y `admin.py` para la administración. Cada router sigue el patrón de fachada ligera del diseño: resuelve la identidad del usuario, valida los datos de entrada, delega en los servicios y devuelve las respuestas HTTP con los códigos diferenciados. El fragmento siguiente muestra la implementación del endpoint de solicitud de diagnóstico del router `inference.py`, que materializa la subida de la radiografía y el encolado del trabajo.

```python
@router.post("/predict")
async def predict(request: Request, file: UploadFile = File(...), model_name: str = Form(...)):
    user_id = get_user_id_from_token(request.cookies.get("access_token"))
    if not user_id:
        return JSONResponse(status_code=401, content={"error": get_text("no_autenticado")})

    if file.content_type not in _ALLOWED_MIME_TYPES:
        return JSONResponse(status_code=400, content={"status": "error", "message": get_text("solo_imagenes")})

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > _MAX_FILE_SIZE:
        return JSONResponse(status_code=400, content={"status": "error", "message": get_text("imagen_muy_grande")})

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    upload_path = os.path.join("static", "uploads", filename)
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job_id = _enqueue_job(user_id, "diagnosis", {
        "model_name": model_name, "image_path": upload_path,
        "lang": get_lang_from_cookie(request),
    })
    position = _queue_position(job_id, "diagnosis")
    return JSONResponse(content={
        "status": "queued", "job_id": job_id, "position": position,
        "message": get_text("diagnostico_encolado").format(position=position),
    })
```

*Código 28.2 - Solicitud de diagnóstico (`routers/inference.py`)*

La implementación del endpoint refleja las decisiones del diseño del subsistema de diagnóstico. La identidad se resuelve mediante el mecanismo común de identificación de SD-001, y las validaciones del tipo MIME y del tamaño se realizan antes de escribir el fichero en disco, de modo que una petición inválida no ocupa espacio ni una posición en la cola. La imagen se conserva en el área de cargas con un nombre basado en la fecha, y el trabajo se encola con un payload serializable que solo contiene el modelo, la ruta de la imagen y el idioma. La respuesta devuelve el estado `queued` con la posición, y el mensaje se localiza mediante el servicio de idioma. Este patrón —resolver la identidad, validar, delegar y responder con códigos diferenciados— se repite en los routers de los demás subsistemas, con las variaciones propias de cada flujo.

## 28.3 Servicios de aplicación

La capa de servicios se implementa en el paquete `services/` y concentra la lógica de aplicación del sistema. Los servicios se organizan por responsabilidad: `auth_service.py` gestiona la criptografía y las sesiones, `lang.py` la internacionalización, `ml_engine.py` y `xai_generator.py` la predicción y la explicabilidad, `pdf_generator.py` los informes del diagnóstico, `mlops_engine.py` y `trainer_engine.py` el laboratorio, `queue_worker.py` el procesamiento asíncrono, `chatbot_service.py` el asistente conversacional y `rate_limiter.py` y `csrf_middleware.py` los mecanismos de seguridad. El fragmento siguiente muestra la implementación de la creación y la verificación de los tokens de sesión del servicio de autenticación.

```python
def create_access_token(user_id: int) -> str:
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=JWT_ACCESS_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id: int) -> str:
    raw_token = secrets.token_urlsafe(48)
    token_hash = _hash_token(raw_token)
    expires_at = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=JWT_REFRESH_EXPIRE_DAYS)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO refresh_tokens (user_id, token_hash, expires_at) VALUES (%s, %s, %s)",
        (user_id, token_hash, expires_at),
    )
    conn.commit()
    conn.close()
    return raw_token
```

*Código 28.3 - Creación de los tokens de sesión (`services/auth_service.py`)*

La implementación de los tokens refleja la política de seguridad de sesiones del diseño. El token de acceso se firma con JWT mediante la clave secreta del entorno e incluye el identificador del usuario y la fecha de expiración; el token de refresco se genera como un valor aleatorio con `secrets.token_urlsafe`, y en la base de datos solo se conserva su hash SHA-256 junto con la expiración, de modo que una credencial reutilizable no se almacena en texto plano. La gestión de la rotación y de la detección de robo, descrita en el capítulo 17, se implementa en las funciones de verificación del mismo servicio, que distinguen el token activo, el revocado dentro del periodo de gracia y el uso de una credencial revocada, revocando todos los tokens del usuario en este último caso.

## 28.4 Persistencia y acceso a los datos

La persistencia se implementa en el módulo `database.py`, que gestiona el pool de conexiones a MySQL y la inicialización del esquema. El acceso a los datos se resuelve mediante un pool de conexiones configurado con las variables de entorno, de modo que las peticiones concurrentes reutilizan las conexiones del pool sin abrir una conexión por operación. El fragmento siguiente muestra la configuración del pool y la inicialización del esquema.

```python
def _get_pool():
    global _pool
    if _pool is None:
        _pool = MySQLConnectionPool(
            pool_name="mypool",
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "tfg_pneumonia"),
        )
    return _pool

def get_db_connection():
    return _get_pool().get_connection()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()
```

*Código 28.4 - Pool de conexiones e inicialización del esquema (`database.py`)*

La implementación de la persistencia refleja el modelo físico del capítulo 19 y la generación del esquema del capítulo 23. El pool se configura con los parámetros del entorno y se crea perezosamente en la primera conexión; la inicialización del esquema ejecuta las sentencias `CREATE TABLE IF NOT EXISTS` de las cinco tablas del sistema —`users`, `consultations`, `training_jobs`, `job_queue` y `refresh_tokens`— de modo que el arranque crea el esquema sin un script de migración manual. Los routers y los servicios obtienen las conexiones mediante la función común, aplican las operaciones y las cierran tras confirmar la transacción, manteniendo la integridad de los datos.

## 28.5 Seguridad transversal

La seguridad transversal del backend se implementa en los servicios `csrf_middleware.py` y `rate_limiter.py`, que se aplican a toda la aplicación mediante el middleware y el limitador configurados en el arranque. La protección CSRF se implementa como un middleware que establece una cookie de token en las peticiones seguras y exige su correspondencia en las peticiones que modifican el estado; las cabeceras de seguridad se añaden a todas las respuestas. El fragmento siguiente muestra la implementación de la protección CSRF.

```python
class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method in SAFE_METHODS or request.url.path in CSRF_EXEMPT_PATHS:
            response = await call_next(request)
            if CSRF_COOKIE_NAME not in request.cookies:
                token = secrets.token_urlsafe(32)
                response.set_cookie(key=CSRF_COOKIE_NAME, value=token, httponly=False, samesite="lax")
            return response

        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        csrf_token = request.headers.get(CSRF_HEADER_NAME)
        if not csrf_cookie or not csrf_token or csrf_cookie != csrf_token:
            return JSONResponse(status_code=403, content={"status": "error", "message": "CSRF validation failed"})

        response = await call_next(request)
        return response
```

*Código 28.5 - Protección CSRF (`services/csrf_middleware.py`)*

La implementación de la protección CSRF refleja los requisitos de seguridad del análisis. Las peticiones seguras —GET, HEAD y OPTIONS— se eximen de la comprobación y establecen la cookie del token si no existe; el endpoint de inicio de sesión se exime porque se limita en frecuencia de forma independiente. Las peticiones que modifican el estado exigen que el token de la cookie coincida con el de la cabecera `x-csrf-token`, que la interfaz envía de forma automática en las peticiones asíncronas; si no coinciden, el middleware responde HTTP 403 sin procesar la petición. Las cabeceras de seguridad se añaden en todas las respuestas, y el limitador de peticiones aplica un límite global de sesenta peticiones por minuto y un límite específico de cinco peticiones por minuto al endpoint de inicio de sesión, en coherencia con las pruebas de protección del capítulo 16.

El backend de vitalXAI queda así codificado de forma coherente con el diseño: la aplicación se compone en el arranque con los mecanismos de seguridad y los routers de los seis subsistemas, la capa HTTP sigue el patrón de fachada ligera, los servicios concentran la lógica de aplicación, la persistencia se resuelve con el pool de conexiones y la inicialización del esquema, y la seguridad transversal protege las peticiones y las respuestas de toda la aplicación. La implementación de la ejecución asíncrona, que constituye el soporte del procesamiento en segundo plano, se describe en el capítulo siguiente.
