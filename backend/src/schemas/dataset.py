from pydantic import BaseModel
from src.schemas.common import ORMModel, Timestamped


class DatasetRead(Timestamped):
    id: str
    name: str
    source: str
    status: str
    row_count: int
    checksum: str
    description: str
    workspace_id: str
    created_by: str


class DatasetCreate(BaseModel):
    name: str
    source: str = "manual"
    description: str = ""
    rows: list[dict] = []


class DatasetList(ORMModel):
    items: list[DatasetRead]
    total: int
