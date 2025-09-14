from dataclasses import replace

from src.core.security.interface import IJWTService
from src.modules.users.domain.ports import IUserReader

from ...application.services import DataTransformerService, PasswordService
from ...domain.dto import RoleDTO, SessionDTO, UserDTO
from ...domain.errors import InvalidCredentials
from ...domain.ports import IRolePermissionReader


class AuthenticateUser:
    def __init__(
        self,
        reader: IRolePermissionReader,
        user_reader: IUserReader,
        password_service: PasswordService,
        data_service: DataTransformerService,
        jwt_service: IJWTService
    ):
        self.reader = reader
        self.user_reader = user_reader
        self.password = password_service
        self.data = data_service
        self.jwt = jwt_service
        
    async def login(self, email: str, password: str) -> UserDTO:
        user = await self.user_reader.get_by_email(email)
        if not user or not self.password.verify_password(password, user.password):
            raise InvalidCredentials()
        
        actions = await self.reader.get_by_role(user.role.role_id)
        permissions = self.data.build_permissions_map(actions)
        menu = self.data.build_menu(actions)
        
        token = self.jwt.encode_token(
            {
                "sub": str(user.person_id),
                "name": f"{user.first_name} {user.last_name}",
                "role": f"{user.role.name}",
                "permissions": permissions,
            }
        )
        session = SessionDTO(permissions=permissions, menu=menu)
        
        response = UserDTO(
            person_id=user.person_id,
            national_id_number=getattr(user, "national_id_number", None),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            photo_url=getattr(user, "photo_url", None),
            phone_number=getattr(user, "phone_number", None),
            role=RoleDTO(user.role.role_id, user.role.name),
            session=session,
        )
        
        return response, token
        