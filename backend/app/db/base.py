# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.category import Category  # noqa
from app.models.comment import Comment  # noqa
from app.models.post import Post  # noqa
from app.models.post_tag import PostTag  # noqa
from app.models.tag import Tag  # noqa
from app.models.user import User  # noqa
