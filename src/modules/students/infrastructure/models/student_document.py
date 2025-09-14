import uuid

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import StatusType


class StudentDocument(Base):
    __tablename__ = "student_documents"
    
    enrolment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "student_enrolments.enrolment_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "documents.document_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    status: Mapped[StatusType] = mapped_column(
        SQLEnum(StatusType, name="status_type_enum"),
        nullable=False,
        default=StatusType.PENDING
    )
    review_notes: Mapped[str] = mapped_column(
        String,
        nullable=True
    )
    