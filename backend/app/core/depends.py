"""
Common FastAPI dependency.
"""
from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.db.session import SessionLocal


def get_session() -> Generator:
    """
    Get database session dependency.

    Returns:
        session: Session
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_current_user(
    session: Session = Depends(get_session),
) -> models.User:
    """
    Authenticate and get current login user.

    Args:
        session: Session. SQLAlchemy ORM session.

    Returns:
        user: User. Current login user.

    Raises:
        HTTPException
    """
    # TODO: parse JWT token in request. Authorize and return login user.
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
    )


def get_current_active_user(
    user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Check current user is active or not. Return active user.

    Args:
        user: User. Current login user.

    Returns:
        user: User

    Raises:
        HTTPException
    """
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user."
        )


def get_current_super_user(
    user: models.User = Depends(get_current_active_user),
) -> models.User:
    """
    Check current user is active and is superuser or not. Return super user.

    Args:
        user: User. Current login user.

    Returns:
        user: User.
    """
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Superuser is required."
        )
