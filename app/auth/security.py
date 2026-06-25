"""
Seguridad: hash de contraseñas y manejo de tokens JWT.

- Hash: bcrypt directamente (compatible con bcrypt>=4.0.0, sin passlib).
- JWT:  PyJWT.
"""
import hashlib
import hmac
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt  # PyJWT
import bcrypt

logger = logging.getLogger("device_systems")

# ── Configuración ─────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "device_systems_secret_key_sena_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# ── Hash de contraseñas ───────────────────────────────────────────────────────

def get_password_hash(password: str) -> str:
    """Genera el hash seguro de una contraseña usando bcrypt."""
    # bcrypt tiene un límite de 72 bytes; truncamos para evitar el ValueError
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña plana coincida con el hash almacenado."""
    if not hashed_password:
        return False
    try:
        password_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except Exception:
        return False


# ── JWT ───────────────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera un token JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica y valida un token JWT. Retorna None si es inválido o expirado."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        logger.debug("Token expirado")
        return None
    except jwt.InvalidTokenError as e:
        logger.debug(f"Token inválido: {e}")
        return None
