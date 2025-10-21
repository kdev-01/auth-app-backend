import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.modules.competition.domain.enums import MatchStatusType


class Match(Base):
    __tablename__ = "matches"

    match_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status: Mapped[MatchStatusType] = mapped_column(
        SQLEnum(MatchStatusType, name="match_status_type_enum"),
        nullable=False,
        default=MatchStatusType.SCHEDULED,
    )
    scheaduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.event_id", ondelete="SET NULL"), nullable=True
    )
    phase_id: Mapped[int] = mapped_column(
        ForeignKey("phases.phase_id", ondelete="SET NULL"), nullable=True
    )
    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.venue_id", ondelete="SET NULL"), nullable=True
    )
