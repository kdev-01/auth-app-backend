from datetime import date
from typing import List

from sqlalchemy import Select, insert, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.dto import AcademicYearDTO
from ..models import AcademicYear


class AcademicYearRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.academic_year = AcademicYear.__table__

    # Utils
    def _row_to_dto(self, row: RowMapping) -> AcademicYearDTO:
        return AcademicYearDTO(
            academic_year_id=row["academic_year_id"],
            start_date=row["start_date"],
            end_date=row["end_date"],
        )

    # Create
    async def create(self, start_date: date, end_date: date) -> AcademicYearDTO:
        query = (
            insert(self.academic_year)
            .values(start_date=start_date, end_date=end_date)
            .returning(self.academic_year.c.academic_year_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one()

    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.academic_year.c.academic_year_id,
                self.academic_year.c.start_date,
                self.academic_year.c.end_date,
            )
            .select_from(self.academic_year)
            .order_by(self.academic_year.c.start_date.desc())
        )

    async def list_all(self) -> List[AcademicYearDTO]:
        result = await self.db.execute(self._base_query())
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
