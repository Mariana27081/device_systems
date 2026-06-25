from fastapi import FastAPI
from app.database.connection import engine
from app.models.user_model import User
from app.routes.user_routes import router as user_router

# Crear tablas automáticamente al iniciar
User.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Incluye persistencia real con SQLAlchemy y SQLite, "
        "validaciones con Pydantic y operaciones CRUD completas."
    ),
    version="3.0.0",
    contact={
        "name": "Soporte Técnico",
        "email": "desarrollo@devicesystems.com",
    }
)

app.include_router(user_router)


@app.get("/", tags=["Root"], summary="Endpoint Raíz")
def read_root():
    return {
        "message": "Bienvenido a device_systems API v3.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }
