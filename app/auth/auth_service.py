from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token
)
from app.models.user_model import User
from app.schemas.auth_schema import (
    UserLogin,
    UserRegister
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user: UserRegister
    ):
        """
        Registra un nuevo usuario con contraseña hasheada.
        """

        existing_user = (
            db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )

        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            role=user.role,
            is_active=user.is_active
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Usuario registrado correctamente."
        }

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin
    ):
        """
        Autentica al usuario con email y contraseña, y genera un token JWT.
        """

        user = (
            db.query(User)
            .filter(User.email == credentials.email)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo."
            )

        if not verify_password(
            credentials.password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos."
            )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @staticmethod
    def get_me(
        current_user: User
    ):
        """
        Retorna los datos del usuario autenticado.
        """

        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at
        }


auth_service = AuthService()