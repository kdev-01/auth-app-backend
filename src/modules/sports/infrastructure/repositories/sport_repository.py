from typing import List

from sqlalchemy import Select, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.dto import SportDTO
from ..models import Sport


class SportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.sport = Sport.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> SportDTO:
        return SportDTO(
            sport_id=row["sport_id"],
            name=row["name"],
        )
        
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.sport.c.sport_id,
                self.sport.c.name,
            ).select_from(
                self.sport
            ).order_by(
                self.sport.c.name.asc(),
            )
        )
    
    async def list_all(self) -> List[SportDTO]:
        result = await self.db.execute(self._base_query())
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
        