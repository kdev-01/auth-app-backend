import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class TournamentInstitution(Base):
    __tablename__ = "tournament_institutions"

    tournament_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tournaments.tournament_id", ondelete="CASCADE"), primary_key=True
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("educational_institutions.institution_id", ondelete="CASCADE"),
        primary_key=True,
    )
