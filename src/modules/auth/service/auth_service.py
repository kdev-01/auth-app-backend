from dataclasses import asdict, is_dataclass
from typing import Mapping

from fastapi import HTTPException, status

from src.core.security import IJWTService
from src.modules.users.domain.ports import IUserReader

from ..application.services.password import PasswordService
from ..infrastructure.repositories.permission_repository import RolePermissionRepository
from .permissions import RolePermissionService


class AuthenticationService:
    def __init__(
        self,
        perm_repo: RolePermissionRepository,
        user_reader: IUserReader | None = None,
        perm_service: RolePermissionService | None = None,
        jwt_service: IJWTService | None = None,
        password_service: PasswordService | None = None,
    ):
        self.perm_repo = perm_repo
        self.user_reader = user_reader
        self.permission = perm_service
        self.jwt = jwt_service
        self.password = password_service
    
    async def _build_user_info(
        self,
        user: dict,
        permissions=None,
        permissions_map=None,
    ) -> dict:
        if is_dataclass(user):
            u = asdict(user)
        elif isinstance(user, Mapping):
            u = dict(user)
        else:
            u = user.__dict__.copy()
        
        pwd = u.pop("password", None) or u.pop("password_hash", None)
        u.setdefault("status", bool(pwd))
        role_id = u.get("role_id")
        if not role_id and isinstance(u.get("role"), dict):
            role_id = u["role"].get("role_id")
            
        if permissions is None:
            permissions = await self.perm_repo.get_permission_by_role(role_id)
            
        if permissions_map is None:
            permissions_map = self.permission.build_permissions_map(permissions)
        
        return {
            **u,
            "permissions": permissions_map,
            "menu": self.permission.build_menu(permissions),
        }
    
    async def authenticate_user(self, email: str, password: str):
        user = await self.user_reader.get_by_email(email)
        if not user or not self.password.verify_password(password, user.password):
            raise HTTPException(
                detail="Correo o contraseña inválidos.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        
        perms = await self.perm_repo.get_permission_by_role(user.role.role_id)
        perms_map = self.permission.build_permissions_map(perms)
        
        token = self.jwt.encode_token(
            {
                "sub": str(user.person_id),
                "name": f"{user.first_name} {user.last_name}",
                "role": f"{user.role.name}",
                "permissions": perms_map,
            }
        )
        
        user = await self._build_user_info(user, permissions=perms, permissions_map=perms_map)
        return user, token
    
    async def get_profile(self, person_id: str) -> dict:
        user = await self.user_reader.get_by_id(person_id)
        if not user:
            raise HTTPException(
                detail="Error interno del servidor",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return await self._build_user_info(user)
    