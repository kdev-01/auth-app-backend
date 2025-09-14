from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CityDTO:
    city_id: int
    name: str
    