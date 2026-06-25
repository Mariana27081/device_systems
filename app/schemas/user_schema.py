from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

ROLES_PERMITIDOS = ["admin", "user", "support"]


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre completo del usuario",
                      examples=["Ana Pérez"])
    email: EmailStr = Field(..., description="Correo electrónico único y válido",
                            examples=["ana@sena.edu.co"])
    role: str = Field(..., description="Rol del usuario: admin, user o support",
                      examples=["user"])
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
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

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

    model_config = {"from_attributes": True}


class UserBasicResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}
