from sqlalchemy import Column, ForeignKey, Integer

from app.db.base_class import Base


class PostTag(Base):
    """
    SQLAlchemy ORM model for "posttag" table database.
    Association table between "post" and "tag" table.
    """

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="CASCADE"))
