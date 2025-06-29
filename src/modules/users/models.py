import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

import pytz
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base

if TYPE_CHECKING:
    from src.modules.auth.models import Role, UserPermission

ecuador_tz = pytz.timezone("America/Guayaquil")


class Person(Base):
    __tablename__ = "persons"

    # Columns
    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    national_id_number: Mapped[str] = mapped_column(String(11), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ecuador_tz),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ecuador_tz),
        onupdate=lambda: datetime.now(ecuador_tz),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        back_populates="person",
        uselist=False,
        cascade="all, delete",
        passive_deletes=True,
    )


class User(Base):
    __tablename__ = "users"

    # Columns
    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.person_id", ondelete="CASCADE"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.role_id", ondelete="CASCADE")
    )

    # Relationships
    person: Mapped["Person"] = relationship(back_populates="user", uselist=False)
    role: Mapped["Role"] = relationship(back_populates="users")
    user_permissions: Mapped[List["UserPermission"]] = relationship(
        back_populates="user", cascade="all, delete", passive_deletes=True
    )
