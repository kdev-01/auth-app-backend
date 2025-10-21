import uuid
from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from ..domain.enums import TournamentLevelType


# Tournament
@dataclass(frozen=True, slots=True)
class TournamentDTO:
    tournament_id: uuid.UUID
    name: str
    start_date: date
    end_date: date
    level: TournamentLevelType
    description: Optional[str] = None


# Academic year
@dataclass(frozen=True, slots=True)
class AcademicYearDTO:
    academic_year_id: int
    start_date: date
    end_date: date
