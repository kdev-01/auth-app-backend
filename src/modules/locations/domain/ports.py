from typing import List, Protocol

from .dto import CityDTO


class ICityReader(Protocol):
    async def list_all(self) -> List[CityDTO]: ...
    