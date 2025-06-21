from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import db_settings

engine = create_async_engine(db_settings.postgresql_url)
session_factory = async_sessionmaker(bind=engine)

