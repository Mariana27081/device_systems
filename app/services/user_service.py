from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from typing import Optional, List


class UserService:

    @staticmethod
    def get_all_users(
        db: Session,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: Optional[str] = None
    ) -> List[User]:
        query = db.query(User)
        if role:
            query = query.filter(User.role == role.lower())
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        if order_by == "name":
            query = query.order_by(asc(User.name))
        elif order_by == "created_at":
            query = query.order_by(desc(User.created_at))
        else:
            query = query.order_by(asc(User.id))
        return query.all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email.lower()).first()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        new_user = User(
            name=user_data.name,
            email=user_data.email.lower(),
            role=user_data.role.lower(),
            is_active=user_data.is_active,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user_complete(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user.name = user_data.name
        user.email = user_data.email.lower()
        user.role = user_data.role.lower()
        user.is_active = user_data.is_active
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user_partial(db: Session, user_id: int, user_data: UserPatch) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value:
                value = value.lower()
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True
