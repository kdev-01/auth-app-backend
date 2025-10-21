from fastapi import Depends

from src.core.database.di import get_uow
from src.core.database.uow_session import SQLAlchemySessionUoW

from ..application.use_cases import GetCities
from ..domain.ports import ICityReader


def provide_list_cities(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> GetCities:
    reader = uow.get(ICityReader)
    return GetCities(reader=reader)
