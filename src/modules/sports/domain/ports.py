from typing import List, Protocol

from ..domain.dto import SportDTO


# Sport
class ISportReader(Protocol):
    async def list_all(self) -> List[SportDTO]: ...
    