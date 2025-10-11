from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class AgeCategory(Base):
    __tablename__ = "age_categories"

    age_category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    min_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    max_age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    