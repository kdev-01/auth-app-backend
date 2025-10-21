from functools import lru_cache
from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.auth.infrastructure.di import register_auth
from src.modules.institutions.infrastructure.di import register_institutions
from src.modules.locations.infrastructure.di import register_cities
from src.modules.sports.infrastructure.di import register_sports
from src.modules.tournaments.infrastructure.di import register_tournaments
from src.modules.users.infrastructure.di import register_users

from .engine import get_sessionmaker
from .uow_session import SQLAlchemySessionUoW


@lru_cache()
def build_repo_registry() -> dict[type[Any], Callable[[AsyncSession], Any]]:
    reg: dict[type[Any], Callable[[AsyncSession], Any]] = {}
    register_auth(reg)
    register_institutions(reg)
    register_cities(reg)
    register_sports(reg)
    register_users(reg)
    register_tournaments(reg)
    return reg


async def get_uow():
    session_factory = get_sessionmaker()
    async with SQLAlchemySessionUoW(
        session_factory, repo_factories=build_repo_registry()
    ) as uow:
        yield uow
