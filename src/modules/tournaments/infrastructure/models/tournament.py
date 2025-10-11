import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import TournamentLevelType
from src.core.timezone import ECUADOR_TZ


class Tournament(Base):
    __tablename__ = "tournaments"

    tournament_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    level: Mapped[TournamentLevelType] = mapped_column(
        SQLEnum(TournamentLevelType, name="tournament_level_type_enum"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ECUADOR_TZ)
    )
    academic_year_id: Mapped[int] = mapped_column(
        ForeignKey("academic_years.academic_year_id", ondelete="SET NULL"),
        nullable=True
    )
    