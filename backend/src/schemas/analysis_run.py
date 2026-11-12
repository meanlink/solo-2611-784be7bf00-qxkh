from datetime import datetime
from pydantic import BaseModel
from src.schemas.common import ORMModel


class RunRead(ORMModel):
    id: str
    status: str
    result: dict
    metrics: list
    error_message: str
    checksum: str
    started_at: datetime | None
    completed_at: datetime | None
    analysis_id: str
    created_by: str
    created_at: datetime


class RunList(ORMModel):
    items: list[RunRead]
    total: int


class CommentCreate(BaseModel):
    body: str
    decision: str = "pending"
