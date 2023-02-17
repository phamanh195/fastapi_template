from typing import Generic, TypeVar

import factory

ModelFactoryType = TypeVar("ModelFactoryType", bound=factory.DictFactory)


class BaseModelFactoryService(Generic[ModelFactoryType]):
    """
    Base class of model factory. Provide methods (CRUD..) for preparing test subject.
    """

    def __init__(self, factory_model: type[ModelFactoryType]):
        """
        Provide methods (CRUD..) for preparing test subject.

        Args:
            factory_model: type[ModelFactoryType]. Factory class of model.
        """
        self.factory_model = factory_model
