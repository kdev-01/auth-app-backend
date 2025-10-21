import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class Tournament(Base):
    __tablename__ = "tournaments"

    tournament_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(300), nullable=False)
    academic_year_id: Mapped[int] = mapped_column(
        ForeignKey("academic_years.academic_year_id", ondelete="SET NULL"),
        nullable=True,
    )
