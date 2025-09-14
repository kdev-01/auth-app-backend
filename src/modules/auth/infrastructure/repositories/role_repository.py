from typing import List

from sqlalchemy import Select, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import Role

from ...domain.dto import RoleDTO


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role = Role.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> RoleDTO:
        return RoleDTO(
            role_id=row["role_id"],
            name=row["name"],
        )
    
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.role.c.role_id,
                self.role.c.name,
            ).select_from(
                self.role
            )
        )
    
    async def list_all(self) ->  List[RoleDTO]:
        result = await self.db.execute(self._base_query())
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
    