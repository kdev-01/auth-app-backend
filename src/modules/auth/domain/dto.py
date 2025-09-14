from dataclasses import dataclass
from typing import Dict, List, Optional
from uuid import UUID


# Role
@dataclass(frozen=True, slots=True)
class RoleDTO:
    role_id: UUID
    name: str

# Role permission
@dataclass(frozen=True, slots=True)
class RPermissionDTO:
    name: str

# Out
@dataclass(frozen=True, slots=True)
class MenuItemDTO:
    name: str
    path: str
    children: Optional[List["MenuItemDTO"]] = None

@dataclass(frozen=True, slots=True)
class SessionDTO:
    permissions: Dict[str, List[str]]
    menu: List[MenuItemDTO]

@dataclass(frozen=True, slots=True)
class UserDTO:
    person_id: UUID
    national_id_number: str
    first_name: str
    last_name: str
    email: str
    photo_url: Optional[str] = None
    phone_number: Optional[str] = None
    role: RoleDTO = None
    session: Optional[SessionDTO] = None
