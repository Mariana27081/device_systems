from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Modelo base con los atributos comunes
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único")
    role: str = Field(..., description="Rol asignado: admin, user o support")
    is_active: bool = Field(default=True, description="Estado de activación del usuario")

# Esquema para crear un usuario (POST)
class UserCreate(UserBase):
    pass  # Hereda todo lo de UserBase

# Esquema para actualizar completamente un usuario (PUT)
class UserUpdate(UserBase):
    pass  # Requiere obligatoriamente todos los campos

# Esquema para actualización parcial (PATCH)
class UserUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

# Esquema de respuesta de la API (Lo que ve el cliente)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True