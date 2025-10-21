import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class User(Base):
    __tablename__ = "users"

    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("persons.person_id", ondelete="CASCADE"), primary_key=True
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True, unique=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.role_id", ondelete="CASCADE")
    )
