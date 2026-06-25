from fastapi import HTTPException, status, Path
from app.services.user_service import UserService

# 1. Dependencia para verificar si un usuario existe por su ID
def get_user_or_404(user_id: int = Path(..., description="ID del usuario a buscar", gt=0)):
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

# 2. Dependencia para validar que un correo electrónico no esté duplicado
def validate_unique_email(email: str):
    user = UserService.get_user_by_email(email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya se encuentra registrado"
        )

# 3. Dependencia para validar que el rol esté dentro de los permitidos
def validate_allowed_role(role: str):
    allowed_roles = ["admin", "user", "support"]
    if role.lower() not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol no permitido. Roles válidos: {', '.join(allowed_roles)}"
        )