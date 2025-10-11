from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SportDTO:
    sport_id: int
    name: str
