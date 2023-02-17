import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from app import models
from app.core.config import Settings
from app.core.depends import get_session
from app.db.base import Base
from app.main import app
from app.tests.factories.user import user_factory_service

# Override testing settings
testing_settings = Settings(POSTGRES_DB=os.environ.get("POSTGRES_TEST_DB", "test_blog"))

# Override testing database
if not database_exists(testing_settings.SQLALCHEMY_DATABASE_URI):
    create_database(testing_settings.SQLALCHEMY_DATABASE_URI)
testing_engine = create_engine(
    testing_settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=testing_engine
)

# Setup the database once
Base.metadata.drop_all(bind=testing_engine)
Base.metadata.create_all(bind=testing_engine)


@pytest.fixture()
def session() -> Session:  # type: ignore[misc]
    """
    This fixture is the main difference to before. It creates a nested
    transaction, recreates it when the application code calls session.commit
    and rolls it back at the end.

    References:
        https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#
        joining-a-session-into-an-external-transaction-such-as-for-test-suites
        https://stackoverflow.com/a/67348153
    """
    connection = testing_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT)
    nested = connection.begin_nested()

    # If the application code calls session.commit,
    # it will end the nested transaction. Need to start a new one when that happens.
    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):  # noqa
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session) -> TestClient:  # type: ignore[misc]
    """
    A fixture for FastAPI test client, which depends on the
    previous session fixture. Instead of creating a new session in the
    dependency override as before, it uses the one provided by the session fixture.
    """

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    del app.dependency_overrides[get_session]


@pytest.fixture()
def user(session: Session) -> models.User:
    """
    Generate a user fixture.

    Args:
        session: Session. SQLAlchemy ORM session.

    Returns:
        user: User.
    """
    user = user_factory_service.create(session=session)
    return user
