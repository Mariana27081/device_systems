from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status

from sqlalchemy.orm import Session

from app.auth.auth_service import auth_service
from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    Token
)
from app.dependencies.auth_dependency import get_current_user
from app.config.limiter import limiter


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    summary="Registrar un nuevo usuario",
    description="Permite registrar un usuario almacenando la contraseña encriptada mediante Passlib (bcrypt).",
    response_description="Usuario registrado correctamente.",
    responses={
        201: {"description": "Usuario registrado correctamente."},
        400: {"description": "El correo ya está registrado."},
        422: {"description": "Datos inválidos."},
        429: {"description": "Demasiadas solicitudes."}
    }
)
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_service.register(
        db,
        user
    )


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica un usuario con email y contraseña, y genera un token JWT.",
    response_description="Token JWT generado correctamente.",
    responses={
        200: {"description": "Inicio de sesión exitoso."},
        401: {"description": "Credenciales inválidas."},
        403: {"description": "Usuario inactivo."},
        429: {"description": "Demasiadas solicitudes."}
    }
)
@limiter.limit("5/minute")
def login(
    request: Request,
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    return auth_service.login(
        db,
        credentials
    )


@router.get(
    "/me",
    summary="Obtener usuario autenticado",
    description="Retorna la información del usuario autenticado mediante el token JWT.",
    response_description="Información del usuario autenticado.",
    responses={
        200: {"description": "Usuario autenticado."},
        401: {"description": "Token inválido o expirado."}
    }
)
def get_me(
    current_user=Depends(get_current_user)
):
    return auth_service.get_me(
        current_user
    )