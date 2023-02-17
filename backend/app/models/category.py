from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .post import Post


class CategoryModelConfig:
    """
    Config for "Category" model database.
    """

    NAME_MAX_LENGTH = 20


class Category(Base):
    """
    SQLAlchemy ORM model for "category" table database.
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(CategoryModelConfig.NAME_MAX_LENGTH), index=True, unique=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="category",
    )
