import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Representative(Base):
    __tablename__ = "representatives"
    
    user_person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "persons.person_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    institution_id: Mapped[int] = mapped_column(
        ForeignKey(
            "educational_institutions.institution_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    unassigned_at: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    