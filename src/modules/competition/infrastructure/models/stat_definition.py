from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class StatDefinition(Base):
    __tablename__ = "stat_definitions"

    stat_definition_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sport_id: Mapped[int] = mapped_column(
        ForeignKey("sports.sport_id", ondelete="SET NULL"), nullable=True
    )
