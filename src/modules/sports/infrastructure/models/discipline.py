from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Discipline(Base):
    __tablename__ = "disciplines"

    discipline_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    sport_category_id: Mapped[int] = mapped_column(
        ForeignKey("sports_categories.sport_category_id", ondelete="SET NULL"),
        nullable=True
    )
    modality_id: Mapped[int] = mapped_column(
        ForeignKey("modalities.modality_id", ondelete="SET NULL"),
        nullable=True
    )
    rule_id: Mapped[int] = mapped_column(
        ForeignKey("rules.rule_id", ondelete="SET NULL"),
        nullable=True
    )
    