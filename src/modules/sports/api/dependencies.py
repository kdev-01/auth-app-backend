from fastapi import Depends

from src.core.database import SQLAlchemySessionUoW, get_uow

from ..application.use_cases import SportRead
from ..domain.ports import ISportReader


def provide_list_sports(
    uow: SQLAlchemySessionUoW = Depends(get_uow)
) -> SportRead:
    reader = uow.get(ISportReader)
    return SportRead(
        reader=reader
    )
    