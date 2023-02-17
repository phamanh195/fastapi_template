from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .post import Post


class TagModelConfig:
    """
    Config for "Tag" model database.
    """

    NAME_MAX_LENGTH = 20


class Tag(Base):
    """
    SQLAlchemy ORM model for "tag" table database.
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(TagModelConfig.NAME_MAX_LENGTH), unique=True)

    # foreign key & relationship
    posts: Mapped[list["Post"]] = relationship("Post", secondary="posttag")
