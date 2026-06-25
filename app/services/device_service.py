from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch
from typing import Optional, List


class DeviceService:

    @staticmethod
    def get_all_devices(
        db: Session,
        device_type: Optional[str] = None,
        is_available: Optional[bool] = None,
        brand: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Device]:
        query = db.query(Device)
        if device_type:
            query = query.filter(Device.device_type == device_type.lower())
        if is_available is not None:
            query = query.filter(Device.is_available == is_available)
        if brand:
            query = query.filter(Device.brand.ilike(f"%{brand}%"))
        if search:
            query = query.filter(
                Device.name.ilike(f"%{search}%") |
                Device.serial_number.ilike(f"%{search}%") |
                Device.brand.ilike(f"%{search}%")
            )
        return query.order_by(asc(Device.id)).all()

    @staticmethod
    def get_device_by_id(db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_device_by_serial(db: Session, serial_number: str) -> Optional[Device]:
        return db.query(Device).filter(Device.serial_number == serial_number.upper()).first()

    @staticmethod
    def create_device(db: Session, device_data: DeviceCreate) -> Device:
        new_device = Device(
            name=device_data.name,
            serial_number=device_data.serial_number.upper(),
            device_type=device_data.device_type.lower(),
            brand=device_data.brand,
            is_available=device_data.is_available,
        )
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device

    @staticmethod
    def update_device_complete(db: Session, device_id: int, device_data: DeviceUpdate) -> Optional[Device]:
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            return None
        device.name = device_data.name
        device.serial_number = device_data.serial_number.upper()
        device.device_type = device_data.device_type.lower()
        device.brand = device_data.brand
        device.is_available = device_data.is_available
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def update_device_partial(db: Session, device_id: int, device_data: DevicePatch) -> Optional[Device]:
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            return None
        update_data = device_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "serial_number" and value:
                value = value.upper()
            setattr(device, field, value)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def delete_device(db: Session, device_id: int) -> bool:
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            return False
        db.delete(device)
        db.commit()
        return True
