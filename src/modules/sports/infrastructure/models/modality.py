from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base
from src.core.database.models.enums import ScoringSystemType


class Modality(Base):
    __tablename__ = "modalities"

    modality_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    is_team: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True
    )
    scoring_system: Mapped[ScoringSystemType] = mapped_column(
        SQLEnum(ScoringSystemType, name="scoring_system_enum"),
        nullable=True
    )
    sport_id: Mapped[int] = mapped_column(
        ForeignKey("sports.sport_id", ondelete="SET NULL"),
        nullable=True
    )
