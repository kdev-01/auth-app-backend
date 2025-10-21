import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class Sanction(Base):
    __tablename__ = "sanctions"

    sanction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    sanction_type_id: Mapped[int] = mapped_column(
        ForeignKey("sanction_types.sanction_type_id", ondelete="SET NULL"),
        nullable=True,
    )
    match_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("matches.match_id", ondelete="SET NULL"), nullable=True
    )
    student_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("students.person_id", ondelete="SET NULL"), nullable=True
    )
