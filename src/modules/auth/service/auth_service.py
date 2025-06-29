from typing import Dict, List

from fastapi import HTTPException, status

from src.modules.users.repository import UserRepository

from .jwt import JWTService
from .password import PasswordService
from .permissions import PermissionsService


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository,
            permissions_service: PermissionsService,
            jwt_service: JWTService,
            password_service: PasswordService,
    ):
        self.user_repo = user_repository
        self.permission = permissions_service
        self.jwt = jwt_service
        self.password = password_service
    
    async def _build_user_info(self, user: dict) -> dict:
        user.pop("password", None)
        permissions = await self.permission.get_list(user["role_id"])
        user["permissions"] = self.permission.build_permissions_map(permissions)
        user["menu"] = self.permission.get_menu(permissions)
        return user
    
    async def get_user_token(self, email: str, password: str) -> tuple[dict, str]:
        user = await self.user_repo.get_user_by_email(email)
        if not user or not self.password.verify_password(password, user["password"]):
            raise HTTPException(
                detail="Correo o contraseña inválidos.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        token = self.jwt.encode_token(
            {
                "sub": str(user["person_id"]),
                "role": str(user["role_id"]),
                "name": f"{user['first_name']} {user['last_name']}",
            }
        )

        user = await self._build_user_info(user)
        return user, token
    
    async def get_user_info(self, person_id: str) -> dict:
        user = await self.user_repo.get_user_by_id(person_id)
        if not user:
            raise HTTPException(
                detail="Error interno del servidor",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return await self._build_user_info(user)
    