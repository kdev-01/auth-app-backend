from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import InstitutionStatusType


class EducationalInstitution(Base):
    __tablename__ = "educational_institutions"
    
    institution_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    status: Mapped[InstitutionStatusType] = mapped_column(
        SQLEnum(InstitutionStatusType, name="institution_status_type_enum"),
        nullable=False,
        default=InstitutionStatusType.AFFILIATED
    )
    photo_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    occurred_at: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )
    created_at: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id", ondelete="SET NULL"),
        nullable=True
    )
    