from typing import Any, Generic, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    BaseService class. Provide default methods(CRUD,..).
    """

    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD)

        Args:
            model: type[ModelType]. A SQLAlchemy model class
        """
        self.model = model

    def get(self, session: Session, _id: Any) -> Optional[ModelType]:
        """
        Get one object of model based on primary key (id).
        Return None if object does not exist.

        Args:
            session: Session. SQLAlchemy ORM Session.
            _id: Any

        Returns:
            obj: ModelType
        """
        return session.query(self.model).filter(self.model.id == _id).first()

    def get_multi(
        self,
        session: Session,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ModelType]:
        """
        Get multiple objects of model. With default limit/offset

        Args:
            session: Session. SQLAlchemy ORM Session.
            offset: int. The number of objects need to skip.
            limit: int. The limit number of objects can be retrieved.

        Returns:
            objs: list[ModelType]
        """
        return session.query(self.model).offset(offset).limit(limit).all()

    def perform_create_update_data(self, obj_in: dict):  # noqa
        """
        Perform create/update subject.

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
        obj_in: Union[CreateSchemaType, dict[str, Any]],
    ) -> ModelType:
        """
        Create object of model (insert to database) based on input object (schema).

        Args:
            session: Session. SQLAlchemy ORM Session.
            obj_in: CreateSchemaType, dict. Create schema object/subject.

        Returns:
            obj: ModelType
        """
        obj_data = jsonable_encoder(obj_in)
        db_obj = self.model(**self.perform_create_update_data(obj_data))
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def bulk_create(
        self,
        session: Session,
        *,
        lst_objs_in: list[Union[CreateSchemaType, dict[str, Any]]],
    ) -> list[ModelType]:
        """
        Bulk create instance of model (insert to database) based on input instance (schema).

        Args:
            session: Session. SQLAlchemy ORM Session.
            lst_objs_in: list[Union[CreateSchemaType, dict[str, Any]]]. List of create schema object/subject.

        Returns:
            objs: list[ModelType]
        """
        lst_objs_data = jsonable_encoder(lst_objs_in)
        db_objs = [
            self.model(**self.perform_create_update_data(obj_data))
            for obj_data in lst_objs_data
        ]
        session.bulk_save_objects(objects=db_objs)
        session.commit()
        return db_objs

    def update(  # noqa
        self,
        session: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        """
        Update object of model (update to database) based on input instance (schema).

        Args:
            session: Session. SQLAlchemy ORM Session.
            db_obj: ModelType. SQLAlchemy ORM object.
            obj_in: Union[UpdateSchemaType, dict[str, Any]]. Update schema object/subject.

        Returns:
            obj: ModelType
        """
        obj_data = jsonable_encoder(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # update to database
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def remove(
        self, session: Session, *, _id: Any = None, db_obj: ModelType = None
    ) -> None:
        """
        Remove object of model (delete from database) based on instance primary key (id).
        By default, function will retrieve and delete object.
        Providing "db_obj" to bypass retrieve step.

        Args:
            session: Session. SQLAlchemy ORM Session.
            _id: Any. Primary key of instance.
            db_obj: Optional[ModelType]. Object of model (optional).
        """
        if not any((_id, db_obj)):
            raise ValueError(
                "Cannot implement. '_id' or 'db_obj' parameter is required."
            )
        if db_obj is None:
            db_obj = session.query(self.model).filter(self.model.id == _id).one()
        session.delete(db_obj)
        session.commit()
        return None
