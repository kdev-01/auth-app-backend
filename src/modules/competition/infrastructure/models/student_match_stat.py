import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class StudentMatchStat(Base):
    __tablename__ = "student_match_stats"

    student_stat_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    value: Mapped[int] = mapped_column(Integer, nullable=True)
    match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("matches.match_id", ondelete="SET NULL"), nullable=True
    )
    student_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("students.person_id", ondelete="SET NULL"), nullable=True
    )
    stat_definition_id: Mapped[int] = mapped_column(
        ForeignKey("stat_definitions.stat_definition_id", ondelete="SET NULL"),
        nullable=True,
    )
