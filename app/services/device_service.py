from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.device_model import Device


def create_device(
    db: Session,
    device
):
    existing = (
        db.query(Device)
        .filter(Device.serial_number == device.serial_number)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado."
        )

    new_device = Device(
        name=device.name,
        serial_number=device.serial_number,
        device_type=device.device_type,
        brand=device.brand
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return new_device


def get_devices(
    db: Session,
    device_type=None,
    brand=None,
    is_available=None,
    search=None
):
    query = db.query(Device)

    valid_types = [
        "laptop",
        "tablet",
        "proyector",
        "cámara",
        "camara",
        "router",
        "monitor"
    ]

    if device_type:
        if device_type.lower() not in valid_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de dispositivo inválido."
            )

        query = query.filter(
            Device.device_type.ilike(f"%{device_type}%")
        )

    if brand:
        query = query.filter(
            Device.brand.ilike(f"%{brand}%")
        )

    if is_available is not None:
        query = query.filter(
            Device.is_available == is_available
        )

    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%")
            )
        )

    return query.all()


def get_device_by_id(
    db: Session,
    device_id: int
):
    device = (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado."
        )

    return device


def update_device(
    db: Session,
    device_id: int,
    device_data
):
    device = get_device_by_id(
        db,
        device_id
    )

    duplicate = (
        db.query(Device)
        .filter(
            Device.serial_number == device_data.serial_number,
            Device.id != device_id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de serie ya está registrado."
        )

    device.name = device_data.name
    device.serial_number = device_data.serial_number
    device.device_type = device_data.device_type
    device.brand = device_data.brand

    db.commit()
    db.refresh(device)

    return device


def patch_device(
    db: Session,
    device_id: int,
    device_data
):
    device = get_device_by_id(
        db,
        device_id
    )

    update_data = device_data.model_dump(
        exclude_unset=True
    )

    if "serial_number" in update_data:
        duplicate = (
            db.query(Device)
            .filter(
                Device.serial_number == update_data["serial_number"],
                Device.id != device_id
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de serie ya está registrado."
            )

    for key, value in update_data.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    return device


def delete_device(
    db: Session,
    device_id: int
):
    device = get_device_by_id(
        db,
        device_id
    )

    db.delete(device)
    db.commit()

    return {
        "message": "Dispositivo eliminado correctamente."
    }