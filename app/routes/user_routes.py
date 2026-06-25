from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin
)

from app.config.limiter import limiter

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserPatch,
    UserResponse
)

from app.schemas.loan_schema import LoanDetailResponse

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    patch_user,
    delete_user
)

from app.services.loan_service import get_user_loans


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un usuario",
    description="Registra un nuevo usuario en el sistema.",
    response_description="Usuario creado correctamente.",
    responses={
        201: {"description": "Usuario creado correctamente."},
        400: {"description": "El correo electrónico ya está registrado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        422: {"description": "Error de validación."}
    }
)
def create(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return create_user(
        db,
        user
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados.",
    response_description="Lista de usuarios.",
    responses={
        200: {"description": "Lista de usuarios obtenida correctamente."},
        401: {"description": "No autenticado."},
        429: {"description": "Demasiadas solicitudes."}
    }
)
@limiter.limit("30/minute")
def list_users(
    request: Request,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    order_by: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_users(
        db,
        role,
        is_active,
        order_by
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario",
    description="Obtiene la información de un usuario por su ID.",
    responses={
        200: {"description": "Usuario encontrado correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Usuario no encontrado."}
    }
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_user_by_id(
        db,
        user_id
    )


@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos de un usuario",
    description="Obtiene el historial de préstamos de un usuario con detalle del dispositivo asociado.",
    responses={
        200: {"description": "Préstamos del usuario obtenidos correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Usuario no encontrado."}
    }
)
def user_loans(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_user_loans(
        db,
        user_id
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza completamente la información de un usuario.",
    responses={
        200: {"description": "Usuario actualizado correctamente."},
        400: {"description": "Correo electrónico duplicado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Usuario no encontrado."}
    }
)
def update(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return update_user(
        db,
        user_id,
        user
    )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar parcialmente un usuario",
    description="Actualiza parcialmente la información de un usuario.",
    responses={
        200: {"description": "Usuario actualizado correctamente."},
        400: {"description": "Correo electrónico duplicado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Usuario no encontrado."}
    }
)
def patch(
    user_id: int,
    user: UserPatch,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    return patch_user(
        db,
        user_id,
        user
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema.",
    responses={
        204: {"description": "Usuario eliminado correctamente."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Usuario no encontrado."}
    }
)
def delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    delete_user(
        db,
        user_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )