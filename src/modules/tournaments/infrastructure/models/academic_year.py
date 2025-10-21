from datetime import date

from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"

    academic_year_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
