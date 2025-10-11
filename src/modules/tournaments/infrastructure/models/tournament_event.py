import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import EventStatusType


class TournamentEvent(Base):
    __tablename__ = "tournament_events"
    
    tournament_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    status: Mapped[EventStatusType] = mapped_column(
        SQLEnum(EventStatusType, name="event_status_type_enum"),
        nullable=False,
        default=EventStatusType.SCHEDULED
    )
    registration_start: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    registration_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )
    tournament_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tournaments.tournament_id", ondelete="CASCADE"),
        nullable=False
    )
    discipline_id: Mapped[int] = mapped_column(
        ForeignKey("disciplines.discipline_id", ondelete="SET NULL"),
        nullable=True
    )
    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.venue_id", ondelete="SET NULL"),
        nullable=True
    )
    