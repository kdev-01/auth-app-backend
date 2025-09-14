from typing import List

from ...domain.dto import RoleDTO
from ...domain.ports import IRoleReader


class RoleRead:
    def __init__(self, reader: IRoleReader):
        self.reader = reader
        
    async def retrieve_all_roles(self) -> List[RoleDTO]:
        return await self.reader.list_all()
