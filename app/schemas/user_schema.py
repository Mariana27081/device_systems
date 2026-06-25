import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator
)


# =====================================================
# Validador de contraseña reutilizable
# =====================================================

def validate_password_rules(value: str) -> str:
    if " " in value:
        raise ValueError(
            "La contraseña no puede contener espacios."
        )

    if len(value) < 8:
        raise ValueError(
            "La contraseña debe tener mínimo 8 caracteres."
        )

    if not re.search(r"[A-Z]", value):
        raise ValueError(
            "La contraseña debe contener al menos una mayúscula."
        )

    if not re.search(r"[a-z]", value):
        raise ValueError(
            "La contraseña debe contener al menos una minúscula."
        )

    if not re.search(r"\d", value):
        raise ValueError(
            "La contraseña debe contener al menos un número."
        )

    return value


# =====================================================
# Schemas
# =====================================================

class UserBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre completo del usuario"
    )

    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario"
    )

    role: Literal[
        "admin",
        "support",
        "user"
    ] = Field(
        default="user",
        description="Rol del usuario"
    )

    is_active: bool = Field(
        default=True,
        description="Estado del usuario"
    )


class UserCreate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Contraseña segura del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_rules(value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@sena.edu.co",
                "password": "Password123",
                "role": "admin",
                "is_active": True
            }
        }
    )


class UserUpdate(UserBase):

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Nueva contraseña del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_rules(value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez Actualizado",
                "email": "juan_actualizado@sena.edu.co",
                "password": "Password123",
                "role": "support",
                "is_active": True
            }
        }
    )


class UserPatch(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Nombre del usuario"
    )

    email: Optional[EmailStr] = Field(
        default=None,
        description="Correo electrónico"
    )

    password: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=100,
        description="Nueva contraseña del usuario"
    )

    role: Optional[
        Literal[
            "admin",
            "support",
            "user"
        ]
    ] = Field(
        default=None,
        description="Rol del usuario"
    )

    is_active: Optional[bool] = Field(
        default=None,
        description="Estado del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_password_rules(value)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "role": "support",
                "is_active": True
            }
        }
    )


class UserResponse(BaseModel):

    id: int = Field(
        ...,
        description="ID del usuario"
    )

    name: str = Field(
        ...,
        description="Nombre del usuario"
    )

    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario"
    )

    role: str = Field(
        ...,
        description="Rol del usuario"
    )

    is_active: bool = Field(
        ...,
        description="Estado del usuario"
    )

    created_at: datetime = Field(
        ...,
        description="Fecha de creación del usuario"
    )

    model_config = ConfigDict(
        from_attributes=True
    )