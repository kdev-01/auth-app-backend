from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models.enums import PermissionType

from ...domain.dto import RPermissionDTO
from ..models import Permission, RolePermission


class RolePermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission = Permission.__table__
        self.rol_per = RolePermission.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> RPermissionDTO:
        return RPermissionDTO(
            name=row["name"],
        )
    
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.permission.c.name
            ).select_from(
                self.rol_per.join(
                    self.permission,
                    self.rol_per.c.permission_id == self.permission.c.permission_id
                )
            ).where(
                self.rol_per.c.type == PermissionType.GRANT
            )
        )
    
    async def get_by_role(self, role_id: UUID) -> list[RPermissionDTO]:
        result = await self.db.execute(
            self._base_query().where(
                    self.rol_per.c.role_id == role_id
                )
            )
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
    