from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class CommentModelConfig:
    """
    Config for "Comment" model database.
    """

    COMMENT_MAX_LENGTH = 255


class Comment(Base):
    """
    SQLAlchemy ORM model for "comment" table database.
    """

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String(CommentModelConfig.COMMENT_MAX_LENGTH), nullable=True)

    # foreign key & relationship
    author_id = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    author: Mapped["User"] = relationship("User")

    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
