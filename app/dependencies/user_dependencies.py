from fastapi import HTTPException
from app.data.users_db import users_db

ALLOWED_ROLES = ["admin", "support", "user"]


def get_user_or_404(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


def validate_role(role: str):
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail="Rol no permitido"
        )


def validate_email_exists(email: str, exclude_user_id: int = None):
    for user in users_db:
        if user["email"] == email:
            if exclude_user_id is None or user["id"] != exclude_user_id:
                raise HTTPException(
                    status_code=400,
                    detail="Correo electrónico duplicado"
                )