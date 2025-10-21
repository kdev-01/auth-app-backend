from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..domain.enums import TournamentLevelType


# Input schemas
class TournamentCreateInput(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    level: TournamentLevelType
    academic_year_id: int


# Output schemas
class AcademicYearOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    academic_year_id: int
    start_date: date
    end_date: date
