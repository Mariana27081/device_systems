from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserBasicResponse
from app.schemas.device_schema import DeviceBasicResponse

LOAN_STATUSES = ["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="ID del usuario al que se presta el dispositivo",
                         examples=[1])
    device_id: int = Field(..., gt=0, description="ID del dispositivo a prestar",
                           examples=[1])


class LoanUpdate(BaseModel):
    status: str = Field(..., description="Nuevo estado del préstamo",
                        examples=["overdue"])

    @field_validator("status")
    @classmethod
    def validar_status(cls, v):
        if v.lower() not in LOAN_STATUSES:
            raise ValueError(f"Estado no válido. Estados permitidos: {', '.join(LOAN_STATUSES)}")
        return v.lower()


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime]
    status: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: datetime
    return_date: Optional[datetime]
    user: UserBasicResponse
    device: DeviceBasicResponse

    model_config = {"from_attributes": True}
