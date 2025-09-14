import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class StudentEnrolment(Base):
    __tablename__ = "student_enrolments"
    
    enrolment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    enrolled_at: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    unenrolled_at: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    user_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.person_id",
            ondelete="SET NULL"
        ),
        nullable=True
    )
    student_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "students.person_id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey(
            "educational_institutions.institution_id",
            ondelete="SET NULL"
        ),
        nullable=True
    )
    