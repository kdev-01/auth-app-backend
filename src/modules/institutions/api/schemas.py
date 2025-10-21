from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from ..domain.enums import InstitutionStatusType


# Input schemas
class InstitutionCreateInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    city_id: Optional[PositiveInt] = None


# Output schemas
class CityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city_id: PositiveInt
    name: str


class InstitutionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    institution_id: PositiveInt
    name: str
    status: InstitutionStatusType
    created_at: date
    occurred_at: Optional[date] = None
    city: Optional[CityOut] = None
