import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import BloodType, GenderType


class Student(Base):
    __tablename__ = "students"
    
    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "persons.person_id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    blood_type: Mapped[BloodType] = mapped_column(
        SQLEnum(BloodType, name="blood_type_enum"),
        nullable=False
    )
    gender: Mapped[GenderType] = mapped_column(
        SQLEnum(GenderType, name="gender_enum"),
        nullable=False
    )
    enrolment_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    