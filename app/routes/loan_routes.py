from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_support_or_admin
)
from app.config.limiter import limiter

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse
)

from app.services.loan_service import (
    create_loan,
    get_loans,
    get_loan_by_id,
    return_device,
    get_loan_details,
    get_user_loans,
    get_device_loans
)

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Asigna un dispositivo disponible a un usuario autenticado.",
    response_description="Préstamo creado correctamente.",
    responses={
        201: {"description": "Préstamo creado correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Usuario o dispositivo no encontrado."},
        409: {"description": "El dispositivo no está disponible."},
        422: {"description": "Error de validación."},
        429: {"description": "Demasiadas solicitudes."}
    }
)
@limiter.limit("10/minute")
def create(
    request: Request,
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return create_loan(
        db,
        loan
    )


@router.get(
    "",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Obtiene todos los préstamos registrados con filtros opcionales.",
    response_description="Lista de préstamos."
)
def read_all(
    status_filter: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_loans(
        db,
        status_filter,
        user_email,
        device_type,
        search
    )


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos con detalles",
    description="Obtiene todos los préstamos con información detallada usando JOIN entre usuarios, dispositivos y préstamos.",
    response_description="Lista de préstamos con detalles.",
    responses={
        200: {"description": "Consulta realizada correctamente."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."}
    }
)
def details(
    db: Session = Depends(get_db),
    current_user=Depends(require_support_or_admin)
):
    return get_loan_details(db)


@router.get(
    "/user/{user_id}",
    response_model=list[LoanDetailResponse],
    summary="Consultar préstamos de un usuario",
    description="Obtiene el historial de préstamos de un usuario específico.",
    response_description="Lista de préstamos del usuario.",
    responses={
        200: {"description": "Consulta realizada correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Usuario no encontrado."}
    }
)
def user_loans(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_user_loans(
        db,
        user_id
    )


@router.get(
    "/device/{device_id}",
    response_model=list[LoanDetailResponse],
    summary="Consultar historial de un dispositivo",
    description="Obtiene el historial de préstamos de un dispositivo específico.",
    response_description="Lista de préstamos del dispositivo.",
    responses={
        200: {"description": "Consulta realizada correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def device_loans(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_device_loans(
        db,
        device_id
    )


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Consultar préstamo por ID",
    description="Obtiene la información detallada de un préstamo específico.",
    response_description="Detalle del préstamo.",
    responses={
        200: {"description": "Consulta realizada correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Préstamo no encontrado."}
    }
)
def read_one(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_loan_by_id(
        db,
        loan_id
    )


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Registrar devolución",
    description="Marca un préstamo como devuelto y libera el dispositivo asociado.",
    response_description="Devolución registrada correctamente.",
    responses={
        200: {"description": "Devolución registrada correctamente."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Préstamo no encontrado."},
        409: {"description": "El préstamo ya fue devuelto."}
    }
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_support_or_admin)
):
    return return_device(
        db,
        loan_id
    )