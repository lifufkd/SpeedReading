from typing import AsyncGenerator
import pytest
from sqlalchemy.testing.pickleable import User

from factories.users import UserFactory
from src.schemas.enums import UsersRoles


@pytest.fixture(scope="function")
async def create_admin(test_session) -> AsyncGenerator[User, None]:
    user = await UserFactory.create(role=UsersRoles.ADMIN)

    yield user

    await test_session.delete(user)
    await test_session.commit()


@pytest.fixture(scope="function")
async def create_user(test_session) -> AsyncGenerator[User, None]:
    user = await UserFactory(role=UsersRoles.USER)

    yield user
