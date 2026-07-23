import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import init_db

# AÑADIMOS 'trainer' a la lista de imports
from routers import auth, history, inference, trainer

app = FastAPI(title="X-Ray AI Consultant")

app.mount("/static", StaticFiles(directory="static"), name="static")
# Añade esta línea debajo de app.mount("/static", ...)
app.mount("/training_results", StaticFiles(directory="training_results"), name="training_results")

app.include_router(auth.router)
app.include_router(history.router)
app.include_router(inference.router)
app.include_router(trainer.router)

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        print("✅ Base de datos conectada e inicializada correctamente.")
    except Exception as e:
        print("==========================================================")
        print("❌ ATENCIÓN: No se pudo conectar a la base de datos MySQL.")
        print("❌ Asegúrate de que XAMPP está abierto y MySQL está en 'Start'.")
        print("==========================================================")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
