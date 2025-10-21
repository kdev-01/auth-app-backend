import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base
from src.core.timezone import ECUADOR_TZ

from ...domain.enums import DocumentType


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type: Mapped[DocumentType] = mapped_column(
        SQLEnum(DocumentType, name="document_type_enum"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(ECUADOR_TZ)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ECUADOR_TZ),
        onupdate=lambda: datetime.now(ECUADOR_TZ),
    )
