"""
device_systems API v3.0.0
API REST segura para gestión de usuarios, dispositivos y préstamos.
Incluye: OAuth2 + JWT, CORS, Middleware personalizado, Rate Limiting, Pydantic v2.
"""
import os
from dotenv import load_dotenv

# ── Cargar variables de entorno ANTES de cualquier otro import ────────────────
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, Base
from app.models import User, Device, Loan  # noqa: F401 – registra todos los modelos
from app.middlewares.request_middleware import RequestMiddleware
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.security_routes import router as security_router
from app.auth.auth_routes import router as auth_router

# ── Crear / actualizar tablas al iniciar ──────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Aplicación FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title="device_systems API",
    description=(
        "API REST **segura** para la gestión de usuarios, dispositivos y préstamos.\n\n"
        "## Autenticación\n"
        "Usa **OAuth2 con JWT Bearer**. Para acceder a rutas protegidas:\n"
        "1. Registra un usuario en `POST /auth/register`.\n"
        "2. Inicia sesión en `POST /auth/login` y obtén el token.\n"
        "3. Haz clic en **Authorize** (candado 🔒) en esta página y pega el token.\n\n"
        "## Roles\n"
        "- **admin** → acceso total.\n"
        "- **support** → puede gestionar dispositivos y devoluciones.\n"
        "- **user** → puede ver información y crear préstamos.\n\n"
        "## Rate Limiting\n"
        "- `/auth/login`: 5 req/min\n"
        "- `/auth/register`: 3 req/min\n"
        "- `GET /users`: 30 req/min\n"
        "- `POST /loans`: 10 req/min"
    ),
    version="3.0.0",
    contact={"name": "Soporte Técnico device_systems", "email": "desarrollo@devicesystems.com"},
    license_info={"name": "SENA - Actividad GA1-220501096-01-AA1-EV11"},
    openapi_tags=[
        {"name": "Auth",     "description": "Registro, login y token JWT"},
        {"name": "Users",    "description": "Gestión de usuarios del sistema"},
        {"name": "Devices",  "description": "Gestión de dispositivos tecnológicos"},
        {"name": "Loans",    "description": "Gestión de préstamos de dispositivos"},
        {"name": "Security", "description": "Información de configuración de seguridad"},
    ],
)

# ── CORS ──────────────────────────────────────────────────────────────────────
_raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Middleware personalizado ──────────────────────────────────────────────────
app.add_middleware(RequestMiddleware)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(security_router)


# ── Endpoint raíz ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"], summary="Endpoint Raíz", include_in_schema=False)
def read_root():
    return {
        "message": "Bienvenido a device_systems API v3.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "resources": {
            "auth":     "/auth",
            "users":    "/users",
            "devices":  "/devices",
            "loans":    "/loans",
            "security": "/security",
        },
    }
