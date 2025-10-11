from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Venue(Base):
    __tablename__ = "venues"
    
    venue_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    photo_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id", ondelete="SET NULL"),
        nullable=True
    )
    