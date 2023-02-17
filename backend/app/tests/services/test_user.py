import copy

import pytest
from sqlalchemy.orm import Session, exc

from app import services
from app.core.security import verify_password
from app.schemas.user import CreateUserSchema, UpdateUserSchema
from app.tests.factories.user import UserFactory, user_factory_service


class TestUserService:
    """
    Test UserService functions.

    Short Terms:
        US: UserService.
    """

    def test_us_create_with_create_schema_success(self, session: Session):
        """
        Test US.create with create schema successfully.
        """
        user_data = UserFactory.build()
        user_in = CreateUserSchema(**user_data)
        user = services.user_service.create(session, obj_in=user_in)

        assert user.name == user_in.name
        assert user.email == user_in.email
        assert user.is_active == user_in.is_active
        assert user.is_superuser == user_in.is_superuser
        assert user.hashed_password
        assert verify_password(
            password=user_in.password, hashed_password=user.hashed_password
        )

    def test_us_update_with_update_schema_success(self, session: Session):
        """
        Test US.update with update schema successfully.
        """
        user = user_factory_service.create(session=session)

        # prepare update subject
        user_update_data = UserFactory.build()
        user_update_schema = UpdateUserSchema(**user_update_data)

        # implement US.update function
        update_user = services.user_service.update(
            session=session, db_obj=user, obj_in=user_update_schema
        )

        # assert subject
        assert update_user.id == user.id
        db_user = services.user_service.get(session=session, _id=user.id)
        assert db_user

        assert db_user.name == user_update_schema.name
        assert db_user.email == user_update_schema.email
        assert verify_password(
            password=user_update_schema.password,
            hashed_password=db_user.hashed_password,
        )

    def test_us_update_with_update_schema_not_change_password_success(
        self, session: Session
    ):
        """
        Test US.update with update schema and not change password success.
        """
        user = user_factory_service.create(session=session)

        # prepare update subject
        user_update_data = UserFactory.build()
        user_update_data.pop("password", None)
        user_update_schema = UpdateUserSchema(**user_update_data)

        # implement US.update function
        update_user = services.user_service.update(
            session=session, db_obj=user, obj_in=user_update_schema
        )

        # assert subject
        assert update_user.id == user.id
        db_user = services.user_service.get(session=session, _id=user.id)
        assert db_user

        assert db_user.name == user_update_schema.name
        assert db_user.email == user_update_schema.email
        # assert not change password
        assert db_user.hashed_password == user.hashed_password

    def test_us_update_with_update_data_success(self, session: Session):
        """
        Test US.update with update subject successfully.
        """
        user = user_factory_service.create(session=session)

        # prepare update subject
        user_update_data = UserFactory.build()

        # implement US.update function
        # use deepcopy because update function will remove the "password" from input.
        update_user = services.user_service.update(
            session=session, db_obj=user, obj_in=copy.deepcopy(user_update_data)
        )

        # assert subject
        assert update_user.id == user.id
        db_user = services.user_service.get(session=session, _id=user.id)
        assert db_user

        assert db_user.name == user_update_data["name"]
        assert db_user.email == user_update_data["email"]
        assert verify_password(
            password=user_update_data["password"],
            hashed_password=db_user.hashed_password,
        )

    def test_us_remove_with_valid_instance_success(self, session: Session):
        """
        Test US.remove with valid instance success.
        """
        user = user_factory_service.create(session=session)

        # implement US.remove function
        services.user_service.remove(session=session, db_obj=user)

        # assert subject
        db_user = services.user_service.get(session=session, _id=user.id)
        assert db_user is None

    def test_us_remove_with_valid_id_success(self, session: Session):
        """
        Test US.remove with valid id success.
        """
        user = user_factory_service.create(session=session)

        # implement US.remove function
        services.user_service.remove(session=session, _id=user.id)

        # assert subject
        db_user = services.user_service.get(session=session, _id=user.id)
        assert db_user is None

    def test_us_remove_with_invalid_id(self, session: Session):
        """
        Test US.remove with invalid id.
        """
        invalid_id = 999

        # implement US.remove function
        with pytest.raises(exc.NoResultFound):
            services.user_service.remove(session=session, _id=invalid_id)
