from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:jcklqo2134@34.39.130.83:5432/postgres")

# Crear el motor de la base de datos
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Crear una fábrica de sesiones asíncronas
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependencia para obtener la sesión
async def get_db():
    async with async_session() as session:
        yield session
