from typing import List, Optional
from uuid import UUID

from sqlalchemy import Select, insert, select, update
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement

from src.modules.auth.infrastructure.models import Role

from ...domain.dto import RoleDTO, UserDTO
from ..models import Person
from ..models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.person = Person.__table__
        self.user = User.__table__
        self.role = Role.__table__

    # Utils
    def _row_to_dto(self, row: RowMapping) -> UserDTO:
        return UserDTO(
            person_id=row["person_id"],
            national_id_number=row.get("national_id_number"),
            first_name=row["first_name"],
            last_name=row["last_name"],
            photo_url=row.get("photo_url"),
            email=row["email"],
            password=row.get("password"),
            phone_number=row.get("phone_number"),
            is_deleted=row["is_deleted"],
            role=RoleDTO(
                role_id=row["role_id"],
                name=row["role_name"],
            ),
        )

    # Create
    async def create(
        self, first_name: str, last_name: str, email: str, role_id: UUID
    ) -> UserDTO:
        insert_person = (
            insert(self.person)
            .values(first_name=first_name, last_name=last_name)
            .returning(self.person.c.person_id)
        )
        result = await self.db.execute(insert_person)
        person_id = result.scalar_one()

        insert_user = insert(self.user).values(
            person_id=person_id, email=email, role_id=role_id
        )
        await self.db.execute(insert_user)
        user = await self.get_by_id(person_id)
        assert user is not None
        return user

    # Read
    def _base_query(self) -> Select:
        return (
            select(
                self.user.c.person_id,
                self.person.c.national_id_number,
                self.person.c.first_name,
                self.person.c.last_name,
                self.person.c.photo_url,
                self.user.c.email,
                self.user.c.password,
                self.user.c.phone_number,
                self.person.c.is_deleted,
                self.user.c.role_id.label("role_id"),
                self.role.c.name.label("role_name"),
            )
            .select_from(
                self.user.join(
                    self.person, self.user.c.person_id == self.person.c.person_id
                ).join(self.role, self.user.c.role_id == self.role.c.role_id)
            )
            .order_by(self.person.c.last_name.asc(), self.person.c.first_name.asc())
        )

    async def list_all(
        self,
        exclude_user_id: UUID,
        include_deleted: bool = True,
    ) -> List[UserDTO]:
        query = self._base_query()

        if include_deleted:
            query = query.where(self.person.c.is_deleted.is_(False))

        if exclude_user_id:
            query = query.where(self.user.c.person_id != exclude_user_id)

        result = await self.db.execute(query)
        rows = result.mappings().all()
        return [self._row_to_dto(r) for r in rows]

    async def _get_one(self, where: ColumnElement[bool]) -> Optional[UserDTO]:
        result = await self.db.execute(self._base_query().where(where))
        row = result.mappings().one_or_none()
        return self._row_to_dto(row) if row else None

    async def get_by_id(self, person_id: UUID) -> Optional[UserDTO]:
        return await self._get_one(self.person.c.person_id == person_id)

    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        return await self._get_one(self.user.c.email == email)

    async def email_exists(self, email: str) -> bool:
        query = select(self.user.c.email).where(self.user.c.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None

    # Update

    # Delete
    async def soft_delete(self, person_id: UUID) -> bool:
        query_person = (
            update(self.person)
            .where(
                self.person.c.person_id == person_id,
                self.person.c.is_deleted.is_(False),
            )
            .values(is_deleted=True)
            .returning(self.person.c.person_id)
        )
        result_person = await self.db.execute(query_person)
        person_row = result_person.fetchone()
        if not person_row:
            return False

        query_user = (
            update(self.user)
            .where(self.user.c.person_id == person_id)
            .values(password=None)
            .returning(self.user.c.person_id)
        )
        result_person = await self.db.execute(query_user)
        user_row = result_person.fetchone()
        if not user_row:
            return False

        return True
