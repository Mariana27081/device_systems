from fastapi import FastAPI
from app.database.connection import engine
from app.models import User, Device, Loan  # noqa: F401 – registers all models
from app.database.connection import Base
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear todas las tablas automáticamente al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios, dispositivos y préstamos en el sistema device_systems. "
        "Incluye persistencia con SQLAlchemy, migraciones con Alembic, relaciones entre modelos "
        "y consultas avanzadas con joins."
    ),
    version="4.0.0",
    contact={
        "name": "Soporte Técnico device_systems",
        "email": "desarrollo@devicesystems.com",
    },
    openapi_tags=[
        {"name": "Users", "description": "Gestión de usuarios del sistema"},
        {"name": "Devices", "description": "Gestión de dispositivos tecnológicos"},
        {"name": "Loans", "description": "Gestión de préstamos de dispositivos"},
    ]
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Endpoint Raíz")
def read_root():
    return {
        "message": "Bienvenido a device_systems API v4.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "resources": {
            "users": "/users",
            "devices": "/devices",
            "loans": "/loans"
        }
    }
