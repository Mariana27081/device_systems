from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description="API REST avanzada para la gestión y control de usuarios del sistema device_systems.",
    version="2.0.0",
    contact={
        "name": "Soporte de Desarrollo Técnico",
        "email": "desarrollo@devicesystems.com",
    }
)

app.include_router(user_router)

@app.get("/", tags=["Root"], summary="Endpoint Raíz")
def read_root():
    return {
        "message": "Bienvenido a device_systems API v2.0.0",
        "docs": "/docs"
    }