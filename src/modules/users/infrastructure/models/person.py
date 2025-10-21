import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.timezone import ECUADOR_TZ


class Person(Base):
    __tablename__ = "persons"

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    national_id_number: Mapped[str] = mapped_column(
        String(11), nullable=True, unique=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ECUADOR_TZ)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ECUADOR_TZ),
        onupdate=lambda: datetime.now(ECUADOR_TZ),
    )
