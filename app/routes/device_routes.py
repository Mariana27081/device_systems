from fastapi import APIRouter, status, Depends, Query, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.device_schema import DeviceResponse, DeviceCreate, DeviceUpdate, DevicePatch
from app.services.device_service import DeviceService
from app.services.loan_service import LoanService
from app.database.connection import get_db

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
)


def get_device_or_404(
    device_id: int = Path(..., description="ID del dispositivo", gt=0),
    db: Session = Depends(get_db)
):
    device = DeviceService.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con ID {device_id} no encontrado"
        )
    return device


@router.get(
    "/",
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Obtiene todos los dispositivos. Soporta filtros por tipo, disponibilidad, marca y búsqueda.",
    response_description="Lista de dispositivos"
)
def list_devices(
    device_type: Optional[str] = Query(None, description="Filtrar por tipo: laptop, tablet, proyector, etc."),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    brand: Optional[str] = Query(None, description="Filtrar por marca"),
    search: Optional[str] = Query(None, description="Buscar en nombre, serial o marca"),
    db: Session = Depends(get_db)
):
    return DeviceService.get_all_devices(
        db, device_type=device_type, is_available=is_available, brand=brand, search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar dispositivo por ID",
    description="Retorna un dispositivo específico por su ID.",
    response_description="Datos del dispositivo"
)
def get_device(device=Depends(get_device_or_404)):
    return device


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo. El número de serie debe ser único.",
    response_description="Dispositivo creado exitosamente"
)
def create_device(device_input: DeviceCreate, db: Session = Depends(get_db)):
    existing = DeviceService.get_device_by_serial(db, device_input.serial_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un dispositivo con el número de serie '{device_input.serial_number}'"
        )
    return DeviceService.create_device(db, device_input)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo completo (PUT)",
    description="Reemplaza todos los campos del dispositivo.",
    response_description="Dispositivo actualizado"
)
def update_device_complete(
    device_input: DeviceUpdate,
    db: Session = Depends(get_db),
    current_device=Depends(get_device_or_404)
):
    if current_device.serial_number != device_input.serial_number.upper():
        existing = DeviceService.get_device_by_serial(db, device_input.serial_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un dispositivo con el número de serie '{device_input.serial_number}'"
            )
    return DeviceService.update_device_complete(db, current_device.id, device_input)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo parcialmente (PATCH)",
    description="Modifica solo los campos enviados.",
    response_description="Dispositivo actualizado parcialmente"
)
def update_device_partial(
    device_input: DevicePatch,
    db: Session = Depends(get_db),
    current_device=Depends(get_device_or_404)
):
    fields = device_input.model_dump(exclude_unset=True)
    if not fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar"
        )
    if device_input.serial_number and current_device.serial_number != device_input.serial_number.upper():
        existing = DeviceService.get_device_by_serial(db, device_input.serial_number)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un dispositivo con el número de serie '{device_input.serial_number}'"
            )
    return DeviceService.update_device_partial(db, current_device.id, device_input)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo de la base de datos.",
    response_description="Sin contenido (eliminación exitosa)"
)
def delete_device(
    db: Session = Depends(get_db),
    current_device=Depends(get_device_or_404)
):
    DeviceService.delete_device(db, current_device.id)


@router.get(
    "/{device_id}/loans",
    status_code=status.HTTP_200_OK,
    summary="Historial de préstamos de un dispositivo",
    description="Consulta todo el historial de préstamos de un dispositivo específico.",
    response_description="Historial de préstamos del dispositivo"
)
def get_device_loans(
    device_id: int = Path(..., gt=0, description="ID del dispositivo"),
    db: Session = Depends(get_db)
):
    device = DeviceService.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con ID {device_id} no encontrado")
    loans = LoanService.get_loans_by_device(db, device_id)
    return [
        {
            "loan_id": l.id,
            "status": l.status,
            "loan_date": l.loan_date,
            "return_date": l.return_date,
            "user": {"id": l.user.id, "name": l.user.name, "email": l.user.email},
            "device": {"id": l.device.id, "name": l.device.name,
                       "serial_number": l.device.serial_number, "device_type": l.device.device_type}
        }
        for l in loans
    ]
