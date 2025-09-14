from fastapi import Depends

from src.core.database.di import SQLAlchemySessionUoW, get_uow

from ..application.use_cases import GetCities
from ..domain.ports import ICityReader


def provide_list_cities(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> GetCities:
    reader = uow.get(ICityReader)
    return GetCities(reader=reader)
