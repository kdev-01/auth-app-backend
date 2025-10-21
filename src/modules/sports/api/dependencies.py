from fastapi import Depends

from src.core.database.di import get_uow
from src.core.database.uow_session import SQLAlchemySessionUoW

from ..application.use_cases import SportRead
from ..domain.ports import ISportReader


def provide_list_sports(uow: SQLAlchemySessionUoW = Depends(get_uow)) -> SportRead:
    reader = uow.get(ISportReader)
    return SportRead(reader=reader)
