from fastapi import Depends

from src.core.config import get_settings
from src.core.database.di import get_uow
from src.core.database.uow_session import SQLAlchemySessionUoW
from src.core.email import IEmailService, provide_email_service
from src.core.security.dependencies import provide_jwt_service
from src.core.security.interface import IJWTService
from src.modules.institutions.domain.ports import (
    IRepresentativeReader,
    IRepresentativeWriter,
)

from ..application.use_cases import InviteUser, UserDelete, UserRead
from ..domain.ports import IUserReader, IUserWriter


def provide_list_users(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> UserRead:
    reader = uow.get(IUserReader)
    representative_reader = uow.get(IRepresentativeReader)
    return UserRead(reader=reader, representative_reader=representative_reader)


def provide_invite_user(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
    email: IEmailService = Depends(provide_email_service),
    jwt: IJWTService = Depends(provide_jwt_service),
) -> InviteUser:
    settings = get_settings()
    reader = uow.get(IUserReader)
    writer = uow.get(IUserWriter)
    representative_writer = uow.get(IRepresentativeWriter)
    return InviteUser(
        reader=reader,
        writer=writer,
        representative_writer=representative_writer,
        email=email,
        jwt=jwt,
        frontend_base_url=settings.FRONTEND_BASE_URL,
        from_email=settings.DEFAULT_FROM_EMAIL,
    )


def provide_delete_user(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
) -> UserDelete:
    reader = uow.get(IUserReader)
    writer = uow.get(IUserWriter)
    representative_writer = uow.get(IRepresentativeWriter)
    return UserDelete(reader, writer, representative_writer)
