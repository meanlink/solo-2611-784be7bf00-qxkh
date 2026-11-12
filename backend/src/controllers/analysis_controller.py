from sqlalchemy.orm import Session

from src.models.workspace import Workspace
from src.schemas.analysis import AnalysisCreate, AnalysisList, AnalysisRead
from src.services import analysis_service, audit_service


def list_items(db: Session) -> AnalysisList:
    items = analysis_service.list_analyses(db)
    return AnalysisList(items=[AnalysisRead.model_validate(item) for item in items], total=len(items))


def create_item(db: Session, payload: AnalysisCreate, user, workspace: Workspace) -> AnalysisRead:
    item = analysis_service.create_analysis(
        db, workspace, user.id, payload.name, payload.dataset_id, payload.kind,
        payload.hypothesis, payload.config
    )
    audit_service.record(db, "analysis.create", "analysis", item.id, user.id, {"kind": item.kind})
    db.commit()
    db.refresh(item)
    return AnalysisRead.model_validate(item)
