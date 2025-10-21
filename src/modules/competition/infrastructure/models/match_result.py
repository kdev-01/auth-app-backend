import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("matches.match_id", ondelete="CASCADE"), primary_key=True
    )
    score_a: Mapped[int] = mapped_column(Integer, nullable=True)
    score_b: Mapped[int] = mapped_column(Integer, nullable=True)
    winner_institution_id: Mapped[int] = mapped_column(
        ForeignKey("educational_institutions.institution_id", ondelete="SET NULL"), nullable=True
    )
