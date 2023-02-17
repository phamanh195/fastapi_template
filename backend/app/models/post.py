from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .category import Category
    from .comment import Comment
    from .tag import Tag
    from .user import User


class PostModelConfig:
    """
    Config for "Post" model database.
    """

    TITLE_MAX_LENGTH = 255
    SHORT_DES_MAX_LENGTH = 255


class Post(Base):
    """
    SQLAlchemy ORM model for "post" table database.
    """

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(PostModelConfig.TITLE_MAX_LENGTH), unique=True)
    short_description = Column(
        String(PostModelConfig.SHORT_DES_MAX_LENGTH), nullable=True
    )
    content = Column(Text(), nullable=True)

    # foreign key & relationship
    author_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    author: Mapped["User"] = relationship("User", back_populates="posts")

    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True
    )
    category: Mapped["Category"] = relationship("Category", back_populates="posts")

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

    tags: Mapped[list["Tag"]] = relationship("Tag", secondary="posttag")
