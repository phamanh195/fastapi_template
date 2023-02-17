import factory
from sqlalchemy.orm import Session

from app.models.user import User, UserModelConfig
from app.schemas.user import CreateUserSchema
from app.services import user_service
from app.tests.factories.base import BaseModelFactoryService
from app.tests.factories.utils import faker, faker_email


class UserFactory(factory.DictFactory):
    """
    Base Factory for "User" model.
    """

    name = factory.LazyAttribute(
        lambda _: faker.unique.name()[: UserModelConfig.NAME_MAX_LENGTH]
    )
    email = factory.LazyAttribute(
        lambda o: faker_email(name=o.name, length=UserModelConfig.EMAIL_MAX_LENGTH)
    )
    password = factory.Faker(
        provider="password",
        length=10,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )


class UserFactoryService(BaseModelFactoryService[UserFactory]):
    """
    Service class provide methods (CRUD..) related to "User" in testing.
    """

    def create(self, session: Session, **kwargs) -> User:
        """
        Generate subject from UserFactory and create user by user_service.create method.
        """
        user_data = self.factory_model.build(**kwargs)
        create_user_schema = CreateUserSchema(**user_data)

        user = user_service.create(session=session, obj_in=create_user_schema)
        return user


user_factory_service = UserFactoryService(factory_model=UserFactory)
