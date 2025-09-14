from typing import List, Protocol
from uuid import UUID

from .dto import RoleDTO, RPermissionDTO


# Role
class IRoleReader(Protocol):
    async def list_all(self) -> List[RoleDTO]: ...
    
# Role permission
class IRolePermissionReader(Protocol):
    async def get_by_role(self, role_id: UUID) -> list[RPermissionDTO]: ...
