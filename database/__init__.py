from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from core.settings import (
    POSTGRESQL_DATABASE_HOST,
    POSTGRESQL_DATABASE_NAME,
    POSTGRESQL_DATABASE_PASSWORD,
    POSTGRESQL_DATABASE_USER,
)

from .models import Base

async_engine: AsyncEngine = create_async_engine(
    f'postgresql+psycopg://{POSTGRESQL_DATABASE_USER}:{POSTGRESQL_DATABASE_PASSWORD}@{POSTGRESQL_DATABASE_HOST}/{POSTGRESQL_DATABASE_NAME}'
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_database_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = ['async_engine', 'async_session', 'create_database_tables']
