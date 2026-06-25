from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from app.dependencies.auth_dependency import get_current_active_user


router = APIRouter(
    prefix="/security",
    tags=["Security"]
)


@router.get(
    "/info",
    summary="Información general de seguridad",
    description="Muestra la configuración general de seguridad implementada en la API."
)
def security_info(
    current_user=Depends(get_current_active_user)
):
    return {
        "application": "device_systems",
        "security": {
            "authentication": "OAuth2 + JWT",
            "password_hash": "Passlib bcrypt",
            "protected_routes": True,
            "cors": True,
            "custom_middleware": True,
            "rate_limiting": True
        },
        "roles": [
            "admin",
            "support",
            "user"
        ],
        "headers": [
            "Authorization: Bearer <token>",
            "X-Request-ID",
            "X-App-Name",
            "X-Process-Time"
        ]
    }


@router.get(
    "/cors",
    summary="Configuración CORS",
    description="Retorna la configuración CORS habilitada para la API."
)
def cors_info(
    current_user=Depends(get_current_active_user)
):
    return {
        "allow_origins": [
            "http://localhost:3000",
            "http://localhost:5173"
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "note": "En producción no se recomienda usar configuraciones demasiado abiertas cuando se manejan credenciales."
    }


@router.get(
    "/headers",
    summary="Cabeceras de seguridad y middleware",
    description="Muestra las cabeceras personalizadas generadas por el middleware global."
)
def headers_info(
    request: Request,
    current_user=Depends(get_current_active_user)
):
    return {
        "request_headers_received": {
            "X-Request-ID": request.headers.get("X-Request-ID")
        },
        "response_headers_expected": {
            "X-App-Name": "device_systems",
            "X-Process-Time": "Tiempo de procesamiento de la petición",
            "X-Request-ID": "Identificador único de la solicitud"
        }
    }


@router.get(
    "/rate-limit",
    summary="Políticas de rate limiting",
    description="Muestra los límites configurados para endpoints sensibles de la API."
)
def rate_limit_info(
    current_user=Depends(get_current_active_user)
):
    return {
        "limits": {
            "POST /auth/register": "3/minute",
            "POST /auth/login": "5/minute",
            "GET /users": "30/minute",
            "POST /loans": "10/minute"
        },
        "error_code_when_exceeded": 429,
        "error_message": "Too Many Requests"
    }