from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


# Input schemas
class UserLoginInput(BaseModel):
    email: EmailStr
    password: str

# Output schemas
class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    role_id: UUID
    name: str

class MenuItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    path: str
    children: Optional[List["MenuItemOut"]] = None

class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    permissions: Dict[str, List[str]]
    menu: List[MenuItemOut]

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    person_id: UUID
    national_id_number: str
    first_name: str
    last_name: str
    photo_url: Optional[HttpUrl] = None
    email: EmailStr
    phone_number: Optional[str] = None
    role: RoleOut = None
    session: SessionOut
