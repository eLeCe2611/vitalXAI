import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

import uvicorn  # noqa: E402
from fastapi import FastAPI  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from slowapi import _rate_limit_exceeded_handler  # noqa: E402
from slowapi.errors import RateLimitExceeded  # noqa: E402

from database import init_db  # noqa: E402

# AÑADIMOS 'trainer' a la lista de imports
from routers import admin, auth, history, inference, queue, trainer  # noqa: E402
from services.csrf_middleware import CSRFMiddleware, SecurityHeadersMiddleware  # noqa: E402
from services.queue_worker import start_worker  # noqa: E402
from services.rate_limiter import limiter  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        print("✅ Base de datos conectada e inicializada correctamente.")
    except Exception:
        print("==========================================================")
        print("❌ ATENCIÓN: No se pudo conectar a la base de datos MySQL.")
        print("❌ Asegúrate de que XAMPP está abierto y MySQL está en 'Start'.")
        print("==========================================================")
    start_worker(app)
    print("✅ Worker de cola iniciado.")
    yield


app = FastAPI(title="X-Ray AI Consultant", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CSRFMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
# Añade esta línea debajo de app.mount("/static", ...)
os.makedirs("training_results", exist_ok=True)
app.mount("/training_results", StaticFiles(directory="training_results"), name="training_results")

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(inference.router)
app.include_router(queue.router)
app.include_router(trainer.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
