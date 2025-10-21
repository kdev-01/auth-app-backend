from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from .enums import InstitutionStatusType


# Educational institution
@dataclass(frozen=True, slots=True)
class CityDTO:
    city_id: int
    name: str


@dataclass(frozen=True, slots=True)
class InstitutionDTO:
    institution_id: int
    name: str
    status: InstitutionStatusType
    created_at: date
    occurred_at: Optional[date]
    city: Optional[CityDTO] = None


# Representative
@dataclass(frozen=True, slots=True)
class RepresentativeDTO:
    user_person_id: UUID
    institution_id: int
    unassigned_at: Optional[date] = None


@dataclass(frozen=True, slots=True)
class InstitutionRepresentativeDTO:
    institution_id: int
    name: str


@dataclass(frozen=True, slots=True)
class RepresentativeAssignmentDTO:
    user_person_id: UUID
    institution: InstitutionRepresentativeDTO
