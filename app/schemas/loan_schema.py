from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class LoanCreate(BaseModel):

    user_id: int = Field(
        ...,
        description="ID del usuario que solicita el préstamo."
    )

    device_id: int = Field(
        ...,
        description="ID del dispositivo que será prestado."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": 1,
                "device_id": 2
            }
        }
    )


class LoanUpdate(BaseModel):

    status: Optional[str] = Field(
        default=None,
        description="Estado del préstamo."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "returned"
            }
        }
    )


class LoanResponse(BaseModel):

    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )


class LoanUser(BaseModel):

    id: int
    name: str
    email: str

    model_config = ConfigDict(
        from_attributes=True
    )


class LoanDevice(BaseModel):

    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]

    model_config = ConfigDict(
        from_attributes=True
    )


class LoanDetailResponse(BaseModel):

    id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    user: LoanUser
    device: LoanDevice

    model_config = ConfigDict(
        from_attributes=True
    )