import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class MatchParticipant(Base):
    __tablename__ = "match_participants"

    match_participant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    side: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey("educational_institutions.institution_id", ondelete="SET NULL"),
        nullable=True,
    )
    match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("matches.match_id", ondelete="CASCADE"),
        nullable=False,
    )
