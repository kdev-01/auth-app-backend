import uuid

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Permission, RolePermission


class RolePermissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission = Permission.__table__
        self.rol_per = RolePermission.__table__
        
    async def get_permission_by_role(self, role_id: uuid.UUID) -> list[str]:
        query = (
            select(
                func.coalesce(
                    func.json_agg(self.permission.c.name),
                    func.cast("[]", JSON)
                ).label("permissions")
            )
            .select_from(self.rol_per.join(
                self.permission, self.rol_per.c.permission_id == self.permission.c.permission_id
                )
            ).where(self.rol_per.c.role_id == role_id)
        )

        result = await self.db.execute(query)
        return result.scalar_one()
    