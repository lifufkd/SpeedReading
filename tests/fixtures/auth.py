import pytest
from httpx import AsyncClient
from fastapi_jwt_auth import AuthJWT

from src.models import Users


@pytest.fixture(scope='function')
async def admin_client(client: AsyncClient, create_admin: Users):
    auth = AuthJWT()

    access_token = auth.create_access_token(
        subject=create_admin.login,
        user_claims={"user_id": create_admin.user_id}
    )
    refresh_token = auth.create_refresh_token(subject=create_admin.login)

    client.cookies.set("access_token_cookie", access_token)
    client.cookies.set("refresh_token_cookie", refresh_token)

    yield client
