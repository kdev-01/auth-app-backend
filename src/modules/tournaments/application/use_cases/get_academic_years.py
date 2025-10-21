from typing import List

from ...domain.dto import AcademicYearDTO
from ...domain.ports import IAcademicYearReader


class AcademicYearRead:
    def __init__(self, reader: IAcademicYearReader):
        self.reader = reader

    async def retrieve_all_academic_years(self) -> List[AcademicYearDTO]:
        return await self.reader.list_all()
