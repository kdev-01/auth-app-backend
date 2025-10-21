from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.enums import TournamentLevelType
from ..models import Tournament


class TournamentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tournament = Tournament.__table__

    # Create
    """async def create(
        self,
        name: str,
        description: Optional[str] = None,
        start_date: datatime,
        end_date: datatime,
        level: TournamentLevelType,
        academic_year_id: int
    ):
        pass"""
