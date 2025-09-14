from typing import List

from ...domain.dto import CityDTO
from ...domain.ports import ICityReader


class GetCities:
    def __init__(self, reader: ICityReader):
        self.reader = reader
        
    async def retrieve_all_cities(self) -> List[CityDTO]:
        return await self.reader.list_all()
    