from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, slots=True)
class InstitutionDTO:
    institution_id: int
    name: str

@dataclass(frozen=True, slots=True)
class RoleDTO:
    role_id: UUID
    name: str
    institution: Optional[InstitutionDTO] = None

@dataclass(frozen=True, slots=True)
class UserDTO:
    person_id: UUID
    national_id_number: Optional[str]
    first_name: str
    last_name: str
    photo_url: Optional[str]
    email: str
    password: str
    phone_number: Optional[str]
    is_deleted: bool
    role: RoleDTO
