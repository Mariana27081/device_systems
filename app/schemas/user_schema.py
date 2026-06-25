from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

ROLES_PERMITIDOS = ["admin", "user", "support"]


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único y válido")
    role: str = Field(..., description="Rol del usuario: admin, user o support")
    is_active: bool = Field(default=True, description="Estado de activación del usuario")

    @field_validator("role")
    @classmethod
    def validar_rol(cls, v):
        if v.lower() not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol no permitido. Roles válidos: {', '.join(ROLES_PERMITIDOS)}")
        return v.lower()

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Nuevo nombre")
    email: Optional[EmailStr] = Field(None, description="Nuevo correo electrónico")
    role: Optional[str] = Field(None, description="Nuevo rol: admin, user o support")
    is_active: Optional[bool] = Field(None, description="Nuevo estado")

    @field_validator("role")
    @classmethod
    def validar_rol(cls, v):
        if v is not None and v.lower() not in ROLES_PERMITIDOS:
            raise ValueError(f"Rol no permitido. Roles válidos: {', '.join(ROLES_PERMITIDOS)}")
        return v.lower() if v else v

    @field_validator("name")
    @classmethod
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else v


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
