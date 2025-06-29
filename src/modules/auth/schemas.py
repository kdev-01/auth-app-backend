from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, HttpUrl


# Input schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Output schemas
class ActionPermissions(BaseModel):
    read: bool = False
    write: bool = False
    update: bool = False
    delete: bool = False
    
class UserInfo(BaseModel):
    person_id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role_id: UUID
    photo_url: Optional[HttpUrl] = None
    permissions: Dict[str, ActionPermissions]
    menu: List[Dict[str, str]]
    