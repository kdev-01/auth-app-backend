from typing import List

from ...domain.dto import SportDTO
from ...domain.ports import ISportReader


class SportRead:
    def __init__(self, reader: ISportReader):
        self.reader = reader
        
    async def retrieve_all_sports(self) -> List[SportDTO]:
        return await self.reader.list_all()
    