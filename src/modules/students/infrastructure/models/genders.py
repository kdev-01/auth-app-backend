from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class Gender(Base):
    __tablename__ = "genders"

    gender_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
