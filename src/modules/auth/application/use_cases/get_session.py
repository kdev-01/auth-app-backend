from typing import List
from uuid import UUID

from src.modules.users.domain.ports import IUserReader

from ...application.services import DataTransformerService
from ...domain.dto import RoleDTO, SessionDTO, UserDTO
from ...domain.ports import IRolePermissionReader


class GetUserSession:
    def __init__(
        self,
        reader: IRolePermissionReader,
        user_reader: IUserReader,
        service: DataTransformerService
    ):
        self.reader = reader
        self.user = user_reader
        self.data = service
    
    async def get_session(self, target_id: UUID) -> UserDTO:
        user = await self.user.get_by_id(target_id)
        actions = await self.reader.get_by_role(user.role.role_id)
        
        permissions = self.data.build_permissions_map(actions)
        menu = self.data.build_menu(actions)
        
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
        
        return response
        