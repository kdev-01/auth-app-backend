import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List

import pytz
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.base import Base

if TYPE_CHECKING:
    from src.modules.users.models import User

ecuador_tz = pytz.timezone("America/Guayaquil")


class PermissionType(PyEnum):
    GRANT = "grant"
    DENY = "deny"


class Role(Base):
    __tablename__ = "roles"

    # Columns
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    users: Mapped[List["User"]] = relationship(
        back_populates="role", cascade="all, delete", passive_deletes=True
    )
    role_permissions: Mapped[List["RolePermission"]] = relationship(
        back_populates="role",
        cascade="all, delete",
        passive_deletes=True,
    )


class Permission(Base):
    __tablename__ = "permissions"

    # Columns
    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    role_permissions: Mapped[List["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete",
        passive_deletes=True,
    )
    user_permissions: Mapped[List["UserPermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete",
        passive_deletes=True,
    )


class RolePermission(Base):
    __tablename__ = "role_permissions"

    # Columns
    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.role_id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True
    )
    type: Mapped[PermissionType] = mapped_column(
        SQLEnum(PermissionType, name="permission_type_enum"),
        nullable=False,
        default=PermissionType.GRANT,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ecuador_tz),
        onupdate=lambda: datetime.now(ecuador_tz),
        nullable=False,
    )

    # Relationships
    role: Mapped["Role"] = relationship(back_populates="role_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="role_permissions")


class UserPermission(Base):
    __tablename__ = "user_permissions"

    # Columns
    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.person_id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True
    )
    type: Mapped[PermissionType] = mapped_column(
        SQLEnum(PermissionType, name="permission_type_enum"),
        nullable=False,
        default=PermissionType.GRANT,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ecuador_tz),
        onupdate=lambda: datetime.now(ecuador_tz),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_permissions")
    permission: Mapped["Permission"] = relationship(back_populates="user_permissions")
