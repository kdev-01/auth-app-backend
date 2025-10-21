from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class Phase(Base):
    __tablename__ = "phases"

    phase_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
