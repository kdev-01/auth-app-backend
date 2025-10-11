from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import GenderType


class SportCategory(Base):
    __tablename__ = "sports_categories"

    sport_category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    gender: Mapped[GenderType] = mapped_column(
        SQLEnum(GenderType, name="gender_enum", create_type=False, native_enum=True),
        nullable=False
    )
    age_category_id: Mapped[int] = mapped_column(
        ForeignKey("age_categories.age_category_id", ondelete="SET NULL"),
        nullable=True
    )
    