import re
from typing import Literal, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator
)


class UserRegister(BaseModel):
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

    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña segura"
    )

    confirm_password: str = Field(
        ...,
        min_length=8,
        description="Confirmación de contraseña"
    )

    role: Literal["admin", "support", "user"] = Field(
        default="user",
        description="Rol del usuario"
    )

    is_active: bool = Field(
        default=True,
        description="Estado del usuario"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
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
                "La contraseña debe contener al menos una letra mayúscula."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "La contraseña debe contener al menos una letra minúscula."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "La contraseña debe contener al menos un número."
            )

        return value

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError(
                "Las contraseñas no coinciden."
            )

        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@gmail.com",
                "password": "Password123",
                "confirm_password": "Password123",
                "role": "admin",
                "is_active": True
            }
        }
    )


class UserLogin(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Correo electrónico"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña del usuario"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "juan@gmail.com",
                "password": "Password123"
            }
        }
    )


class Token(BaseModel):
    access_token: str = Field(
        ...,
        description="Token JWT de acceso"
    )

    token_type: str = Field(
        default="bearer",
        description="Tipo de token"
    )

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenData(BaseModel):
    email: Optional[str] = Field(
        default=None,
        description="Correo electrónico del usuario autenticado"
    )

    role: Optional[str] = Field(
        default=None,
        description="Rol del usuario autenticado"
    )

    model_config = ConfigDict(
        from_attributes=True
    )