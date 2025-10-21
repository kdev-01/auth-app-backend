import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base

from ...domain.enums import BloodType


class Student(Base):
    __tablename__ = "students"

    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.person_id", ondelete="CASCADE"), primary_key=True
    )
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    blood_type: Mapped[BloodType] = mapped_column(
        SQLEnum(BloodType, name="blood_type_enum"), nullable=False
    )
    enrolment_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    gender_id: Mapped[int] = mapped_column(
        ForeignKey("genders.gender_id", ondelete="SET NULL"), nullable=True
    )
