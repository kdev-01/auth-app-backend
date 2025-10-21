import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.timezone import ECUADOR_TZ

from ...domain.enums import PermissionType


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True
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
        default=lambda: datetime.now(ECUADOR_TZ),
        onupdate=lambda: datetime.now(ECUADOR_TZ),
        nullable=False,
    )
