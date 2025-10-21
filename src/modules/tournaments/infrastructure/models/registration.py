import uuid

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base

from ...domain.enums import StatusType


class Registration(Base):
    __tablename__ = "registrations"

    registration_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    status: Mapped[StatusType] = mapped_column(
        SQLEnum(StatusType, name="status_type_enum"),
        nullable=False,
        default=StatusType.PENDING,
    )
    review_notes: Mapped[str] = mapped_column(String, nullable=True)
    user_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.person_id", ondelete="SET NULL"), nullable=True
    )
    student_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("students.person_id", ondelete="SET NULL"), nullable=True
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.event_id", ondelete="CASCADE"), nullable=True
    )
