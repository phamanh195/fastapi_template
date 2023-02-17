from fastapi import status
from fastapi.testclient import TestClient

from app import models
from app.tests.utils.authentication import force_authentication


class TestPingPublic:
    """
    Test ping/public API. This API is public for all users (include anonymous..)
    """

    endpoint_url = "/api/v1/ping/public"

    def test_ping_public_with_anonymous_success(self, client: TestClient):
        """
        Test ping_public API success.
        """
        response = client.get(self.endpoint_url)

        assert response.status_code == status.HTTP_200_OK


class TestPingPrivate:
    """
    Test ping/private API. This API limits only login users.
    """

    endpoint_url = "api/v1/ping/private"

    def test_ping_private_with_anonymous_fail(self, client: TestClient):
        """
        Test ping_private API with anonymous user and expect fail response.
        """
        response = client.get(self.endpoint_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_ping_private_with_user_success(
        self,
        client: TestClient,
        user: models.User,
    ):
        """
        Test ping_private API with login user success.
        """
        # create user and force login to system
        with force_authentication(client=client, user=user):
            # call api and assert response
            response = client.get(self.endpoint_url)

            assert response.status_code == status.HTTP_200_OK, response.content
