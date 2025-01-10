from fastapi import FastAPI
from routers.auth import router as auth_router
from models.db import engine
from sqlalchemy.sql import text  # Importar text
app = FastAPI()

# Registrar las rutas de autenticación
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup():
    # Verifica la conexión a la base de datos al iniciar
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
