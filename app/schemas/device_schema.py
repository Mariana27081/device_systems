from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

DEVICE_TYPES = ["laptop", "tablet", "proyector", "camara", "router", "monitor", "otro"]


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Nombre del dispositivo",
                      examples=["Laptop Lenovo ThinkPad"])
    serial_number: str = Field(..., min_length=3, max_length=100,
                               description="Número de serie único del dispositivo",
                               examples=["LEN-2024-001"])
    device_type: str = Field(..., description="Tipo de dispositivo",
                             examples=["laptop"])
    brand: Optional[str] = Field(None, max_length=100, description="Marca del dispositivo",
                                  examples=["Lenovo"])
    is_available: bool = Field(default=True, description="Disponibilidad del dispositivo")

    @field_validator("device_type")
    @classmethod
    def validar_tipo(cls, v):
        if v.lower() not in DEVICE_TYPES:
            raise ValueError(f"Tipo no válido. Tipos permitidos: {', '.join(DEVICE_TYPES)}")
        return v.lower()

    @field_validator("serial_number")
    @classmethod
    def validar_serial(cls, v):
        if not v.strip():
            raise ValueError("El número de serie no puede estar vacío")
        return v.strip().upper()


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DevicePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    serial_number: Optional[str] = Field(None, min_length=3, max_length=100)
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None

    @field_validator("device_type")
    @classmethod
    def validar_tipo(cls, v):
        if v is not None and v.lower() not in DEVICE_TYPES:
            raise ValueError(f"Tipo no válido. Tipos permitidos: {', '.join(DEVICE_TYPES)}")
        return v.lower() if v else v


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DeviceBasicResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}
