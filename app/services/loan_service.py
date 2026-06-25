from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User


def create_loan(
    db: Session,
    loan
):

    user = db.query(User).filter(
        User.id == loan.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    device = db.query(Device).filter(
        Device.id == loan.device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado."
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El dispositivo no está disponible."
        )

    new_loan = Loan(
        user_id=loan.user_id,
        device_id=loan.device_id,
        status="active"
    )

    device.is_available = False

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan


def get_loans(
    db: Session,
    status_filter=None,
    user_email=None,
    device_type=None,
    search=None
):

    query = (
        db.query(Loan)
        .join(User)
        .join(Device)
    )

    valid_status = [
        "active",
        "returned",
        "overdue"
    ]

    if status_filter:

        if status_filter not in valid_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado de préstamo inválido."
            )

    filters = []

    if status_filter:
        filters.append(
            Loan.status == status_filter
        )

    if user_email:
        filters.append(
            User.email.ilike(f"%{user_email}%")
        )

    if device_type:
        filters.append(
            Device.device_type.ilike(f"%{device_type}%")
        )

    if filters:
        query = query.filter(
            and_(*filters)
        )

    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%")
            )
        )

    return query.all()


def get_loan_by_id(
    db: Session,
    loan_id: int
):

    loan = db.query(Loan).filter(
        Loan.id == loan_id
    ).first()

    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Préstamo no encontrado."
        )

    return loan


def return_device(
    db: Session,
    loan_id: int
):

    loan = get_loan_by_id(
        db,
        loan_id
    )

    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El préstamo ya fue devuelto."
        )

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)

    device = db.query(Device).filter(
        Device.id == loan.device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado."
        )

    device.is_available = True

    db.commit()
    db.refresh(loan)

    return loan


def get_loan_details(
    db: Session
):

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .all()
    )


def get_user_loans(
    db: Session,
    user_id: int
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .filter(User.id == user_id)
        .all()
    )


def get_device_loans(
    db: Session,
    device_id: int
):

    device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dispositivo no encontrado."
        )

    return (
        db.query(Loan)
        .join(User)
        .join(Device)
        .filter(Device.id == device_id)
        .all()
    )