from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.common import IdMixin, TimestampMixin


class Workspace(IdMixin, TimestampMixin, Base):
    __tablename__ = "workspaces"
    natural_key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150))
    client_name: Mapped[str] = mapped_column(String(180))
    context_note: Mapped[str] = mapped_column(Text, default="")
    owner_id: Mapped[str] = mapped_column(String(36), index=True)
