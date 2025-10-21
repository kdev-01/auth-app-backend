from typing import List, Protocol
from .dto import AcademicYearDTO


# Academic year
class IAcademicYearReader(Protocol):
    async def list_all(self) -> List[AcademicYearDTO]: ...
