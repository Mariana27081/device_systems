from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin,
    require_support_or_admin
)

from app.schemas.device_schema import (
    DeviceCreate,
    DevicePut,
    DeviceUpdate,
    DeviceResponse
)

from app.schemas.loan_schema import LoanDetailResponse

from app.services.device_service import (
    create_device,
    get_devices,
    get_device_by_id,
    update_device,
    patch_device,
    delete_device
)

from app.services.loan_service import get_device_loans

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo tecnológico.",
    responses={
        201: {"description": "Dispositivo creado correctamente."},
        400: {"description": "Número de serie duplicado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        422: {"description": "Error de validación."}
    }
)
def create(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_support_or_admin)
):
    return create_device(
        db,
        device
    )


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos registrados."
)
def read_all(
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = Query(default=None),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_devices(
        db,
        device_type,
        brand,
        is_available,
        search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo",
    description="Obtiene la información de un dispositivo por su ID.",
    responses={
        200: {"description": "Dispositivo encontrado correctamente."},
        401: {"description": "No autenticado."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def read_one(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    return get_device_by_id(
        db,
        device_id
    )


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Historial de préstamos",
    description="Obtiene el historial de préstamos asociados a un dispositivo.",
    responses={
        200: {"description": "Historial de préstamos obtenido correctamente."},
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


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo",
    description="Actualiza completamente la información de un dispositivo.",
    responses={
        200: {"description": "Dispositivo actualizado correctamente."},
        400: {"description": "Número de serie duplicado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def update(
    device_id: int,
    device: DevicePut,
    db: Session = Depends(get_db),
    current_user=Depends(require_support_or_admin)
):
    return update_device(
        db,
        device_id,
        device
    )


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar parcialmente dispositivo",
    description="Actualiza parcialmente la información de un dispositivo.",
    responses={
        200: {"description": "Dispositivo actualizado correctamente."},
        400: {"description": "Número de serie duplicado."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def patch(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_support_or_admin)
):
    return patch_device(
        db,
        device_id,
        device
    )


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema.",
    responses={
        204: {"description": "Dispositivo eliminado correctamente."},
        401: {"description": "No autenticado."},
        403: {"description": "Permisos insuficientes."},
        404: {"description": "Dispositivo no encontrado."}
    }
)
def delete(
    device_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    delete_device(
        db,
        device_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )