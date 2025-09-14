from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import get_settings


@lru_cache()
def get_engine():
    settings = get_settings()
    return create_async_engine(settings.ASYNC_DATABASE_URL, echo=False)

@lru_cache()
def get_sessionmaker():
    return async_sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )

# Quitar a futuro
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()
