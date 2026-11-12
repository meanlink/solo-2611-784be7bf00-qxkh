from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.models.common import IdMixin, TimestampMixin


class Comment(IdMixin, TimestampMixin, Base):
    __tablename__ = "comments"
    natural_key: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    body: Mapped[str] = mapped_column(Text)
    decision: Mapped[str] = mapped_column(String(24), default="pending")
    run_id: Mapped[str] = mapped_column(String(36), index=True)
    author_id: Mapped[str] = mapped_column(String(36), index=True)
