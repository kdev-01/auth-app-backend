from fastapi import Depends

from src.core.database.di import get_uow
from src.core.database.uow_session import SQLAlchemySessionUoW

from ..application.use_cases import AcademicYearRead
from ..domain.ports import IAcademicYearReader


def provide_list_academic_years(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> AcademicYearRead:
    reader = uow.get(IAcademicYearReader)
    return AcademicYearRead(reader=reader)
