from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate
from typing import Optional, List


class LoanService:

    @staticmethod
    def get_all_loans(
        db: Session,
        status: Optional[str] = None,
        user_email: Optional[str] = None,
        device_type: Optional[str] = None,
        user_id: Optional[int] = None,
        device_id: Optional[int] = None,
    ) -> List[Loan]:
        query = db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        )
        if status:
            query = query.filter(Loan.status == status.lower())
        if user_email:
            query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))
        if device_type:
            query = query.join(Device).filter(Device.device_type == device_type.lower())
        if user_id:
            query = query.filter(Loan.user_id == user_id)
        if device_id:
            query = query.filter(Loan.device_id == device_id)
        return query.order_by(Loan.id).all()

    @staticmethod
    def get_loan_by_id(db: Session, loan_id: int) -> Optional[Loan]:
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.id == loan_id).first()

    @staticmethod
    def get_loans_by_user(db: Session, user_id: int) -> List[Loan]:
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.user_id == user_id).all()

    @staticmethod
    def get_loans_by_device(db: Session, device_id: int) -> List[Loan]:
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.device_id == device_id).all()

    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
        # Mark device as unavailable
        device = db.query(Device).filter(Device.id == loan_data.device_id).first()
        device.is_available = False

        new_loan = Loan(
            user_id=loan_data.user_id,
            device_id=loan_data.device_id,
            loan_date=datetime.utcnow(),
            status="active",
        )
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        # Reload with relationships
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.id == new_loan.id).first()

    @staticmethod
    def return_loan(db: Session, loan_id: int) -> Optional[Loan]:
        loan = db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.id == loan_id).first()
        if not loan:
            return None
        loan.status = "returned"
        loan.return_date = datetime.utcnow()
        # Mark device as available again
        device = db.query(Device).filter(Device.id == loan.device_id).first()
        device.is_available = True
        db.commit()
        db.refresh(loan)
        return db.query(Loan).options(
            joinedload(Loan.user),
            joinedload(Loan.device)
        ).filter(Loan.id == loan_id).first()
