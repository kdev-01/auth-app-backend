from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Imported from external modules
from src.core.dependencies import get_db
from src.modules.users.repository import UserRepository

# Defined within this module
from .repository import RolePermissionRepository
from .service.auth_service import AuthService
from .service.jwt import JWTService
from .service.password import PasswordService
from .service.permissions import PermissionsService


def get_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    role_permission_repository = RolePermissionRepository(db)
    permissions_service = PermissionsService(role_permission_repository)
    jwt_service = JWTService()
    password_service = PasswordService()
    
    return AuthService(
        user_repository,
        permissions_service,
        jwt_service,
        password_service
    )
