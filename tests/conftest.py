import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.api.v1.router import api_v1_router
from src.database.base import OrmBase
from src.database.session import get_session
from src.core.config import db_settings
from factories.users import UserFactory

from fixtures.users import create_admin, create_user
from fixtures.auth import admin_client


test_engine = create_async_engine(
    url=db_settings.test_async_postgresql_url,
    echo=False,
    poolclass=NullPool
)

test_session_factory = async_sessionmaker(
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession
)


# Drop all tables after each test
@pytest.fixture(scope="session", autouse=True)
async def async_db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(OrmBase.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(OrmBase.metadata.drop_all)


@pytest.fixture(scope="session")
async def test_session(async_db_engine):
    async with test_session_factory() as session:
        await session.begin()

        yield session

        await session.rollback()


@pytest.fixture(scope="function", autouse=True)
def set_session_for_factories(test_session):
    UserFactory._meta.sqlalchemy_session = test_session


@pytest.fixture(scope="function")
async def setup_fastapi_session(test_session):
    def override_get_db():
        yield test_session

    app = FastAPI()
    app.include_router(api_v1_router, prefix="/api/v1")
    app.dependency_overrides[get_session] = override_get_db

    yield app


@pytest.fixture(scope="function")
async def client(setup_fastapi_session):
    async with AsyncClient(transport=ASGITransport(app=setup_fastapi_session), base_url="http://test/api/v1") as ac:
        yield ac
