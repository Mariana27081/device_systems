from fastapi import APIRouter, status, Depends, Query, HTTPException
from typing import List, Optional
from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate, UserUpdatePartial
from app.services.user_service import UserService
from app.dependencies.user_dependencies import get_user_or_404, validate_unique_email, validate_allowed_role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK,
            summary="Listar usuarios", description="Obtiene la lista de todos los usuarios.")
def list_users(
    role: Optional[str] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado")
):
    return UserService.get_all_users(role, is_active)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
            summary="Consultar usuario por ID", description="Busca un usuario por su ID.")
def get_user(user=Depends(get_user_or_404)):
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             summary="Crear usuario", description="Registra un nuevo usuario.")
def create_user(user_input: UserCreate):
    validate_unique_email(user_input.email)
    validate_allowed_role(user_input.role)
    return UserService.create_user(user_input)

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
            summary="Actualización completa", description="Reemplaza todos los datos del usuario.")
def update_user_complete(user_input: UserUpdate, current_user=Depends(get_user_or_404)):
    user_id = current_user["id"]
    if current_user["email"].lower() != user_input.email.lower():
        validate_unique_email(user_input.email)
    validate_allowed_role(user_input.role)
    return UserService.update_user_complete(user_id, user_input)

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK,
              summary="Actualización parcial", description="Modifica solo los campos enviados.")
def update_user_partial(user_input: UserUpdatePartial, current_user=Depends(get_user_or_404)):
    user_id = current_user["id"]
    if not user_input.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    if user_input.email and current_user["email"].lower() != user_input.email.lower():
        validate_unique_email(user_input.email)
    if user_input.role:
        validate_allowed_role(user_input.role)
    return UserService.update_user_partial(user_id, user_input)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK,
               summary="Eliminar usuario", description="Elimina permanentemente un usuario.")
def delete_user(current_user=Depends(get_user_or_404)):
    user_id = current_user["id"]
    UserService.delete_user(user_id)
    return {"message": f"El usuario con ID {user_id} fue eliminado correctamente"}