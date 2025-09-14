from typing import List

from ...domain.dto import InstitutionDTO
from ...domain.ports import IInstitutionsReader


class InstitutionRead:
    def __init__(self, reader: IInstitutionsReader):
        self.reader = reader
    
    async def retrieve_all_institutions(self) -> List[InstitutionDTO]:
        return await self.reader.list_all()
    