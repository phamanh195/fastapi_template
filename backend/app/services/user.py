from typing import Any, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import generate_hashed_password, verify_password
from app.models.user import User
from app.schemas.user import CreateUserSchema, UpdateUserSchema
from app.services.base import BaseService


class UserService(BaseService[User, CreateUserSchema, UpdateUserSchema]):
    """
    UserService class. Provide methods related to "User" model.
    """

    def perform_create_update_data(self, obj_in: dict):
        """
        Perform input subject. Generate hashed_password from provided password.

        Args:
            obj_in: dict

        Returns:
            performed_ins_in: dict
        """
        return obj_in

    def create(
        self,
        session: Session,
        *,
        obj_in: Union[CreateUserSchema, dict[str, Any]],
    ) -> User:
        """
        Create user object based on user subject / user input subject.
        Generate hashed_password from provided password.

        Args:
            session: Session. SQLAlchemy ORM Session.
            obj_in: Union[CreateUserSchema, dict[str, Any]]. User subject or input user schema.

        Returns:
            object: User.
        """
        instance_data = jsonable_encoder(obj_in)

        password = instance_data.pop("password")
        hashed_password = generate_hashed_password(password=password)

        instance_data["hashed_password"] = hashed_password
        return super().create(session=session, obj_in=instance_data)

    def update(  # noqa
        self,
        session: Session,
        *,
        db_obj: User,
        obj_in: Union[UpdateUserSchema, dict[str, Any]],
    ) -> User:
        """
        Update user instance based on user subject / user input subject.
        Generate and update hashed_password if input has password.

        Args:
            session: Session. SQLAlchemy ORM Session.
            db_obj: User. User ORM instance.
            obj_in: Union[UpdateUserSchema, dict[str, Any]]. Update user schema / update subject.

        Returns:
            instance: User.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = generate_hashed_password(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(session=session, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def verify_user_password(user: User, password: str) -> bool:
        """
        Verify "password" is valid for user or not.

        Args:
            user: User.
            password: str.

        Returns:
            is_valid: bool.
        """
        return verify_password(password=password, hashed_password=user.hashed_password)


user_service = UserService(model=User)
