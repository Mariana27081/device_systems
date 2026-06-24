from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre completo")
    email: EmailStr = Field(..., description="Correo electrónico único")
    role: str = Field(..., description="Rol: admin, user o support")
    is_active: bool = Field(default=True, description="Estado de activación")

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True