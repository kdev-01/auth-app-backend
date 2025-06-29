from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


# Input schemas
class PersonEntity(BaseModel):
    national_id_number: str
    first_name: str
    last_name: str
    photo_url: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserEntity(PersonEntity, UserLogin):
    phone_number: Optional[str] = None
    role_id: UUID


class UserAccess(BaseModel):
    first_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: str


# Output schemas
