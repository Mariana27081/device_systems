from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class DeviceBase(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre del dispositivo"
    )

    serial_number: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Número de serie único del dispositivo"
    )

    device_type: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Tipo de dispositivo (laptop, tablet, monitor, router, cámara, etc.)"
    )

    brand: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Marca del dispositivo"
    )


class DeviceCreate(DeviceBase):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2026-001",
                "device_type": "laptop",
                "brand": "Lenovo"
            }
        }
    )


class DevicePut(DeviceBase):

    is_available: bool = Field(
        ...,
        description="Indica si el dispositivo está disponible para préstamo"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Dell Latitude",
                "serial_number": "DEL-2026-002",
                "device_type": "laptop",
                "brand": "Dell",
                "is_available": True
            }
        }
    )


class DeviceUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Nombre del dispositivo"
    )

    serial_number: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="Número de serie"
    )

    device_type: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        description="Tipo del dispositivo"
    )

    brand: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Marca del dispositivo"
    )

    is_available: Optional[bool] = Field(
        default=None,
        description="Disponibilidad del dispositivo"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "brand": "Dell",
                "is_available": True
            }
        }
    )


class DeviceResponse(DeviceBase):

    id: int = Field(
        ...,
        description="ID del dispositivo"
    )

    is_available: bool = Field(
        ...,
        description="Indica si el dispositivo está disponible para préstamo"
    )

    created_at: datetime = Field(
        ...,
        description="Fecha de creación del dispositivo"
    )

    model_config = ConfigDict(
        from_attributes=True
    )