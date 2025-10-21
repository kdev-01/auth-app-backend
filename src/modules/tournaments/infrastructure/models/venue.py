from typing import Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base

from ...domain.enums import VenueStatusType, VenueSurfaceType


class Venue(Base):
    __tablename__ = "venues"

    venue_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[VenueStatusType] = mapped_column(
        SQLEnum(VenueStatusType, name="venue_status_type_enum"),
        nullable=False,
        default=VenueStatusType.AVAILABLE,
    )
    surface: Mapped[VenueSurfaceType] = mapped_column(
        SQLEnum(VenueSurfaceType, name="venue_surface_type_enum"),
        nullable=False,
    )
    length_meters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    width_meters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id", ondelete="SET NULL"), nullable=True
    )
