from pydantic import BaseModel
from src.schemas.common import ORMModel, Timestamped


class AnalysisRead(Timestamped):
    id: str
    name: str
    kind: str
    status: str
    hypothesis: str
    config: dict
    dataset_id: str
    workspace_id: str
    created_by: str


class AnalysisCreate(BaseModel):
    name: str
    dataset_id: str
    kind: str = "primary"
    hypothesis: str = ""
    config: dict = {}


class AnalysisList(ORMModel):
    items: list[AnalysisRead]
    total: int
