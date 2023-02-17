from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Any, expires_delta: timedelta = None) -> str:
    """
    Create access token (JWT token) by encoding and encrypting JSON object (data|dict).

    Args:
        subject: dict. Date need to encode.
        expires_delta: timedelta. Expires time of token.

    Returns:
        access_token: str
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.AUTH_ALGORITH
    )
    return encoded_jwt


def generate_hashed_password(password: str) -> str:
    """
    Encrypt and keep password secret with hash algorithm.

    Args:
        password: str

    Returns:
        hashed_password: str
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify password with hashed_password.

    Args:
        password: str.
        hashed_password: str.

    Returns:
        is_valid: bool.
    """
    return pwd_context.verify(password, hashed_password)
