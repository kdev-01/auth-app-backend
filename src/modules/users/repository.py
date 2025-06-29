import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import ColumnElement

from .models import Person, User
from .schemas import PersonEntity, UserEntity


class PersonRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: PersonEntity) -> Person:
        new_person = Person(
            national_id_number=data.national_id_number,
            first_name=data.first_name,
            last_name=data.last_name,
            photo_url=data.photo_url,
        )
        self.db.add(new_person)
        await self.db.flush()
        return new_person


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.person_repo = PersonRepository(db)
        self.person = Person.__table__
        self.user = User.__table__

    async def create(self, data: UserEntity) -> User:
        new_person = await self.person_repo.create(data)

        new_user = User(
            person_id=new_person.person_id,
            email=data.email,
            password=data.password,
            phone_number=data.phone_number,
            role_id=data.role_id,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user
    
    async def get_user_filter(self, where_clause: ColumnElement) -> dict | None:
        query = (
            select(
                self.user.c.person_id,
                self.person.c.first_name,
                self.person.c.last_name,
                self.user.c.email,
                self.user.c.password,
                self.user.c.role_id,
                self.person.c.photo_url,
            )
            .select_from(
                self.user.join(
                    self.person, self.user.c.person_id == self.person.c.person_id
                )
            ).where(where_clause)
        )
        
        result = await self.db.execute(query)
        row = result.one_or_none()
        return dict(row._mapping) if row else None
    
    async def get_user_by_id(self, person_id: uuid.UUID) -> dict | None:
        return await self.get_user_filter(self.person.c.person_id == person_id)

    async def get_user_by_email(self, email: str) -> dict | None:
        return await self.get_user_filter(self.user.c.email == email)
