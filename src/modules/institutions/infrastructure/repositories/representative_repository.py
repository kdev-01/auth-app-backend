from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import Date, Select, cast, func, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.dto import (
    InstitutionRepresentativeDTO,
    RepresentativeAssignmentDTO,
    RepresentativeDTO,
)
from ..models import EducationalInstitution, Representative


class RepresentativeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.representative = Representative.__table__
        self.institution = EducationalInstitution.__table__
    
    # Utils
    def _row_to_dto(self, row: RowMapping) -> RepresentativeDTO:
        return RepresentativeDTO(
            user_person_id=row["user_person_id"],
            institution_id=row.get("institution_id"),
            unassigned_at=row["unassigned_at"],
        )
    
    def _row_to_assignment_dto(self, row: RowMapping) -> RepresentativeAssignmentDTO:
        return RepresentativeAssignmentDTO(
            user_person_id=row["user_person_id"],
            institution=InstitutionRepresentativeDTO(
                institution_id=row["institution_id"],
                name=row["name"],
            )
        )
    
    # Create
    async def create(
        self,
        user_person_id: UUID,
        institution_id: int,
        unassigned_at: Optional[date] = None,
    ) -> bool:
        query = (
            pg_insert(self.representative)
            .values(
                user_person_id=user_person_id,
                institution_id=institution_id,
                unassigned_at=unassigned_at
            )
        )
        
        """.on_conflict_do_nothing(
                index_elements=[self.representative.c.user_person_id, self.representative.c.institution_id]
        )""" 
        
        result = await self.db.execute(query)
        return result.rowcount == 1
    
    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.representative.c.user_person_id,
                self.representative.c.institution_id,
                self.representative.c.unassigned_at,
            ).select_from(
                self.representative
            )
        )
    
    def _query_with_institution(self) -> Select:
        return (
            select(
                self.representative.c.user_person_id,
                self.institution.c.institution_id,
                self.institution.c.name,
            ).select_from(
                self.representative
                .join(
                    self.institution,
                    self.representative.c.institution_id == self.institution.c.institution_id
                )
            )
        )
    
    async def get_current_assignments(self, person_ids: List[UUID]) -> List[RepresentativeAssignmentDTO]:
        query = (
            self._query_with_institution()
            .where(self.representative.c.unassigned_at.is_(None))
            .where(self.representative.c.user_person_id.in_(person_ids))
        )
        result = await self.db.execute(query)
        rows = result.mappings().all()
        return [self._row_to_assignment_dto(r) for r in rows]
    
    # Delete
    async def unassign_active(self, user_person_id: UUID) -> bool:
        query = (
            update(self.representative)
            .where(
                self.representative.c.user_person_id == user_person_id,
                self.representative.c.unassigned_at.is_(None),
            )
            .values(unassigned_at=cast(func.now(), Date))
        )
        result = await self.db.execute(query)
        return result.rowcount == 1
    