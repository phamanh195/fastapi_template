from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .post import Post


class UserModelConfig:
    """
    Config for "User" model database.
    """

    NAME_MAX_LENGTH = 255
    EMAIL_MAX_LENGTH = 255


class User(Base):
    """
    SQLAlchemy ORM model for "user" table database.
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(UserModelConfig.NAME_MAX_LENGTH), index=True)
    email = Column(
        String(UserModelConfig.EMAIL_MAX_LENGTH),
        unique=True,
        index=True,
        nullable=False,
    )
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
    )
