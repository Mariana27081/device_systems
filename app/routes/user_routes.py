from fastapi import APIRouter, status, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserPatch
from app.services.user_service import UserService
from app.database.connection import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_or_404(
    user_id: int = Path(..., description="ID del usuario", gt=0),
    db: Session = Depends(get_db)
):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Obtiene todos los usuarios. Permite filtrar por rol, estado y ordenar.",
    response_description="Lista de usuarios registrados"
)
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, user o support"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query(None, description="Ordenar por: name o created_at"),
    db: Session = Depends(get_db)
):
    return UserService.get_all_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Retorna un usuario específico buscado por su ID.",
    response_description="Datos del usuario encontrado"
)
def get_user(user=Depends(get_user_or_404)):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. El email debe ser único.",
    response_description="Usuario creado exitosamente"
)
def create_user(user_input: UserCreate, db: Session = Depends(get_db)):
    existing = UserService.get_user_by_email(db, user_input.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado"
        )
    return UserService.create_user(db, user_input)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo (PUT)",
    description="Reemplaza todos los campos del usuario.",
    response_description="Usuario actualizado"
)
def update_user_complete(
    user_input: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_user_or_404)
):
    if current_user.email.lower() != user_input.email.lower():
        existing = UserService.get_user_by_email(db, user_input.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado"
            )
    return UserService.update_user_complete(db, current_user.id, user_input)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente (PATCH)",
    description="Modifica solo los campos enviados en el body.",
    response_description="Usuario actualizado parcialmente"
)
def update_user_partial(
    user_input: UserPatch,
    db: Session = Depends(get_db),
    current_user=Depends(get_user_or_404)
):
    fields = user_input.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    if user_input.email and current_user.email.lower() != user_input.email.lower():
        existing = UserService.get_user_by_email(db, user_input.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado"
            )
    return UserService.update_user_partial(db, current_user.id, user_input)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario de la base de datos.",
    response_description="Sin contenido (eliminación exitosa)"
)
def delete_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_user_or_404)
):
    UserService.delete_user(db, current_user.id)


@router.get(
    "/{user_id}/loans",
    status_code=status.HTTP_200_OK,
    summary="Préstamos de un usuario",
    description="Consulta todos los préstamos asociados a un usuario específico.",
    response_description="Lista de préstamos del usuario",
    tags=["Users"]
)
def get_user_loans(
    user_id: int = Path(..., gt=0, description="ID del usuario"),
    db: Session = Depends(get_db)
):
    from app.services.loan_service import LoanService
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
    loans = LoanService.get_loans_by_user(db, user_id)
    return [
        {
            "loan_id": l.id,
            "status": l.status,
            "loan_date": l.loan_date,
            "return_date": l.return_date,
            "user": {"id": l.user.id, "name": l.user.name, "email": l.user.email},
            "device": {"id": l.device.id, "name": l.device.name,
                       "serial_number": l.device.serial_number, "device_type": l.device.device_type}
        }
        for l in loans
    ]
