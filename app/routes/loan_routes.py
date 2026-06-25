from fastapi import APIRouter, status, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.loan_schema import LoanCreate, LoanResponse
from app.services.loan_service import LoanService
from app.services.user_service import UserService
from app.services.device_service import DeviceService
from app.database.connection import get_db

router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
)


def loan_to_detail(loan):
    return {
        "loan_id": loan.id,
        "status": loan.status,
        "loan_date": loan.loan_date,
        "return_date": loan.return_date,
        "user": {
            "id": loan.user.id,
            "name": loan.user.name,
            "email": loan.user.email
        },
        "device": {
            "id": loan.device.id,
            "name": loan.device.name,
            "serial_number": loan.device.serial_number,
            "device_type": loan.device.device_type
        }
    }


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos",
    description=(
        "Obtiene todos los préstamos con información completa de usuario y dispositivo. "
        "Soporta filtros por estado, email de usuario y tipo de dispositivo."
    ),
    response_description="Lista de préstamos con detalle"
)
def list_loans(
    status: Optional[str] = Query(None, description="Filtrar por estado: active, returned, overdue"),
    user_email: Optional[str] = Query(None, description="Filtrar por email del usuario"),
    device_type: Optional[str] = Query(None, description="Filtrar por tipo de dispositivo"),
    db: Session = Depends(get_db)
):
    loans = LoanService.get_all_loans(
        db, status=status, user_email=user_email, device_type=device_type
    )
    return [loan_to_detail(l) for l in loans]


@router.get(
    "/details",
    status_code=status.HTTP_200_OK,
    summary="Listado detallado de préstamos",
    description="Retorna todos los préstamos con join completo de usuario y dispositivo.",
    response_description="Listado detallado"
)
def list_loans_details(db: Session = Depends(get_db)):
    loans = LoanService.get_all_loans(db)
    return [loan_to_detail(l) for l in loans]


@router.get(
    "/{loan_id}",
    status_code=status.HTTP_200_OK,
    summary="Consultar préstamo por ID",
    description="Retorna los detalles completos de un préstamo específico.",
    response_description="Detalles del préstamo"
)
def get_loan(
    loan_id: int = Path(..., gt=0, description="ID del préstamo"),
    db: Session = Depends(get_db)
):
    loan = LoanService.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con ID {loan_id} no encontrado"
        )
    return loan_to_detail(loan)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description=(
        "Registra un nuevo préstamo. Valida que el usuario y dispositivo existan "
        "y que el dispositivo esté disponible. Marca el dispositivo como no disponible."
    ),
    response_description="Préstamo creado exitosamente"
)
def create_loan(loan_input: LoanCreate, db: Session = Depends(get_db)):
    # Validar usuario
    user = UserService.get_user_by_id(db, loan_input.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {loan_input.user_id} no encontrado"
        )

    # Validar dispositivo
    device = DeviceService.get_device_by_id(db, loan_input.device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {loan_input.device_id} no encontrado"
        )

    # Validar disponibilidad
    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El dispositivo '{device.name}' no está disponible para préstamo"
        )

    loan = LoanService.create_loan(db, loan_input)
    return loan_to_detail(loan)


@router.patch(
    "/{loan_id}/return",
    status_code=status.HTTP_200_OK,
    summary="Devolver dispositivo",
    description=(
        "Marca el préstamo como devuelto, registra la fecha de devolución "
        "y restaura la disponibilidad del dispositivo."
    ),
    response_description="Préstamo actualizado con devolución registrada"
)
def return_loan(
    loan_id: int = Path(..., gt=0, description="ID del préstamo"),
    db: Session = Depends(get_db)
):
    loan = LoanService.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con ID {loan_id} no encontrado"
        )
    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este préstamo ya fue devuelto anteriormente"
        )
    updated_loan = LoanService.return_loan(db, loan_id)
    return loan_to_detail(updated_loan)
