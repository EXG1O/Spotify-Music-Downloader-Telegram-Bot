from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from core.settings import DATABASE_URL

async_engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

__all__ = ['async_engine', 'async_session']
