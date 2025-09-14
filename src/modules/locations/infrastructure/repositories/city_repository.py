from typing import List

from sqlalchemy import Select, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.models import City

from ...domain.dto import CityDTO


class CityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.city = City.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> CityDTO:
        return CityDTO(
            city_id=row["city_id"],
            name=row["name"],
        )
        
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.city.c.city_id,
                self.city.c.name,
            ).select_from(
                self.city
            ).order_by(self.city.c.name.asc())
        )
        
    async def list_all(self) -> List[CityDTO]:
        query = self._base_query()
        result = await self.db.execute(query)
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
    