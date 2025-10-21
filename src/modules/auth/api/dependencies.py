from functools import lru_cache

from fastapi import Depends

from src.core.database.di import get_uow
from src.core.database.uow_session import SQLAlchemySessionUoW
from src.core.security import IJWTService, provide_jwt_service
from src.modules.users.domain.ports import IUserReader

from ..application.services import DataTransformerService, PasswordService
from ..application.use_cases import AuthenticateUser, GetUserSession, RoleRead
from ..domain.ports import IRolePermissionReader, IRoleReader


@lru_cache
def provide_password_service() -> PasswordService:
    return PasswordService()


@lru_cache
def provide_data_service() -> DataTransformerService:
    return DataTransformerService()


def provider_user_session(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
    service: DataTransformerService = Depends(provide_data_service),
) -> GetUserSession:
    reader = uow.get(IRolePermissionReader)
    user_reader = uow.get(IUserReader)
    return GetUserSession(reader=reader, user_reader=user_reader, service=service)


def provider_list_roles(uow: SQLAlchemySessionUoW = Depends(get_uow)) -> RoleRead:
    reader = uow.get(IRoleReader)
    return RoleRead(reader=reader)


def provider_authenticate_user(
    uow: SQLAlchemySessionUoW = Depends(get_uow),
    password_service: PasswordService = Depends(provide_password_service),
    data_service: DataTransformerService = Depends(provide_data_service),
    jwt_service: IJWTService = Depends(provide_jwt_service),
) -> AuthenticateUser:
    reader = uow.get(IRolePermissionReader)
    user_reader = uow.get(IUserReader)
    return AuthenticateUser(
        reader=reader,
        user_reader=user_reader,
        password_service=password_service,
        data_service=data_service,
        jwt_service=jwt_service,
    )
