import uuid
from typing import Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import UnitType


class Rule(Base):
    __tablename__ = "rules"

    rule_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    value: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    unit: Mapped[UnitType] = mapped_column(
        SQLEnum(UnitType, name="unit_type_enum"),
        nullable=False,
    )
    