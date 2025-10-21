import uuid

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.base import Base


class SanctionType(Base):
    __tablename__ = "sanction_types"

    sanction_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
