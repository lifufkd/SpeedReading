from sqlalchemy.ext.asyncio import AsyncEngine

import src.models  # noqa
from src.database.session import engine
from src.database.base import OrmBase


async def create_tables(_engine: AsyncEngine = engine):
    async with _engine.begin() as conn:
        await conn.run_sync(OrmBase.metadata.create_all)
