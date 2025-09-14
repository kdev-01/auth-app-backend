from fastapi import Depends

from src.core.database import SQLAlchemySessionUoW, get_uow

from ..application.use_cases import (
    InstitutionCreate,
    InstitutionDelete,
    InstitutionRead,
)
from ..domain.ports import IInstitutionsReader, IInstitutionsWriter


def provide_list_institutions(
    uow: SQLAlchemySessionUoW = Depends(get_uow)
) -> InstitutionRead:
    reader = uow.get(IInstitutionsReader)
    return InstitutionRead(
        reader=reader
    )

def provider_create_institution(
    uow: SQLAlchemySessionUoW = Depends(get_uow)
) -> InstitutionCreate:
    reader = uow.get(IInstitutionsReader)
    writer = uow.get(IInstitutionsWriter)
    return InstitutionCreate(
        reader=reader,
        writer=writer
    )

def provide_delete_institution(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> InstitutionDelete:
    reader = uow.get(IInstitutionsReader)
    writer = uow.get(IInstitutionsWriter)
    return InstitutionDelete(
        reader=reader,
        writer=writer
    )
