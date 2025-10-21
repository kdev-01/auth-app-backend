from typing import Annotated, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, StringConstraints

OnlyLetters = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$"
Name = Annotated[
    str,
    StringConstraints(
        min_length=1, max_length=50, pattern=OnlyLetters, strip_whitespace=True
    ),
]


# Input schemas
class UserInvite(BaseModel):
    email: EmailStr
    first_name: Name
    last_name: Name
    role_id: UUID
    institution_id: Optional[int] = None


class UserCreate(UserInvite):
    national_id_number: str = Field(..., min_length=10, max_length=11)
    password: str = Field(..., min_length=6)
    phone_number: Optional[str] = Field(None, max_length=20)
    photo_url: Optional[HttpUrl] = None


# Output schemas
class PersonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    person_id: UUID
    national_id_number: Optional[str] = None
    first_name: str
    last_name: str
    photo_url: Optional[HttpUrl] = None


class InstitutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    institution_id: int
    name: str


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_id: UUID
    name: str
    institution: Optional[InstitutionOut] = None


class UserOut(PersonOut):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    phone_number: Optional[str] = None
    is_deleted: bool
    role: RoleOut
