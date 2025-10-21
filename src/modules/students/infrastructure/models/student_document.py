import uuid

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class StudentDocument(Base):
    __tablename__ = "student_documents"

    registration_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("registrations.registration_id", ondelete="CASCADE"),
        primary_key=True,
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.document_id", ondelete="CASCADE"), primary_key=True
    )
