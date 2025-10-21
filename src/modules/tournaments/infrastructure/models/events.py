import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.timezone import ECUADOR_TZ

from ...domain.enums import EventStatusType


class Event(Base):
    __tablename__ = "events"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[EventStatusType] = mapped_column(
        SQLEnum(EventStatusType, name="event_status_type_enum"),
        nullable=False,
        default=EventStatusType.SCHEDULED,
    )
    registration_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    registration_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ECUADOR_TZ)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ECUADOR_TZ),
        onupdate=lambda: datetime.now(ECUADOR_TZ),
    )
    tournament_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tournaments.tournament_id", ondelete="SET NULL"), nullable=True
    )
    gender_id: Mapped[int] = mapped_column(
        ForeignKey("genders.gender_id", ondelete="SET NULL"), nullable=True
    )
    age_category_id: Mapped[int] = mapped_column(
        ForeignKey("age_categories.age_category_id", ondelete="SET NULL"), nullable=True
    )
    sport_id: Mapped[int] = mapped_column(
        ForeignKey("sports.sport_id", ondelete="SET NULL"), nullable=True
    )
