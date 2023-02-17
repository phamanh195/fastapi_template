import contextlib
from collections.abc import Generator

from fastapi.testclient import TestClient

from app import models
from app.core.depends import get_current_user


@contextlib.contextmanager
def force_authentication(
    client: TestClient, user: models.User
) -> Generator[TestClient, None, None]:
    """
    Force authentication with user by overriding "get_current_user" depend.
    """

    def override_get_current_user():  # noqa
        yield user

    client.app.dependency_overrides[get_current_user] = override_get_current_user  # type: ignore
    yield client
    del client.app.dependency_overrides[get_current_user]  # type: ignore
