from typing import List, Optional

from sqlalchemy import Date, Select, cast, func, insert, select, update
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement

from src.core.database.models import City
from src.core.database.models.enums import InstitutionStatusType

from ...domain.dto import CityDTO, InstitutionDTO
from ..models import EducationalInstitution


class InstitutionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.institution = EducationalInstitution.__table__
        self.city = City.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> InstitutionDTO:
        city = None
        if row["city_id"] is not None:
            city = CityDTO(
                city_id=row["city_id"],
                name=row["city_name"],
            )
        return InstitutionDTO(
            institution_id=row["institution_id"],
            name=row["name"],
            status=row["status"],
            created_at=row["created_at"],
            occurred_at=row["occurred_at"],
            city=city
        )
    
    # Create
    async def create(
        self,
        name: str,
        city_id: Optional[int] = None,
    ) -> InstitutionDTO:
        query = (
            insert(self.institution)
            .values(
                name=name,
                city_id=city_id
            )
            .returning(self.institution.c.institution_id)
        )
        result = await self.db.execute(query)
        institution_id = result.scalar_one()
        institution = await self.get_by_id(institution_id)
        assert institution is not None
        return institution
    
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.institution.c.institution_id,
                self.institution.c.name,
                self.institution.c.status,
                self.institution.c.created_at,
                self.institution.c.occurred_at,
                self.city.c.city_id.label("city_id"),
                self.city.c.name.label("city_name"),
            ).select_from(
                self.institution.outerjoin(
                    self.city,
                    self.institution.c.city_id == self.city.c.city_id
                )
            ).order_by(self.institution.c.status.asc(), self.institution.c.name.asc())
        )
    
    async def list_all(self) -> List[InstitutionDTO]:
        result = await self.db.execute(self._base_query())
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]
    
    async def _get_one(self, where: ColumnElement[bool]) -> Optional[InstitutionDTO]:
        result = await self.db.execute(self._base_query().where(where))
        row = result.mappings().one_or_none()
        return self._row_to_dto(row) if row else None
    
    async def get_by_id(self, institution_id: int) -> Optional[InstitutionDTO]:
        return await self._get_one(self.institution.c.institution_id == institution_id)
    
    async def get_by_name(self, name: str) -> Optional[InstitutionDTO]:
        return await self._get_one(func.lower(self.institution.c.name) == name.lower())
    
    # Delete
    async def soft_delete(self, institution_id: int) -> bool:
        query = (
            update(self.institution)
            .where(
                self.institution.c.institution_id == institution_id,
                self.institution.c.occurred_at.is_(None),
            )
            .values(
                status=InstitutionStatusType.UNAFFILIATED,
                occurred_at=cast(func.now(), Date)
            )
            .returning(self.institution.c.institution_id)
        )
        
        result = await self.db.execute(query)
        row = result.fetchone()
        if not row:
            return False
        
        return True
        