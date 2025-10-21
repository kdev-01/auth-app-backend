import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class EventRule(Base):
    __tablename__ = "event_rules"

    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True
    )
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.rule_id", ondelete="CASCADE"), primary_key=True
    )
