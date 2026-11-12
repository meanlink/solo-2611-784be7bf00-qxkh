from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.analysis import Analysis
from src.models.workspace import Workspace


def list_analyses(db: Session) -> list[Analysis]:
    return list(db.scalars(select(Analysis).order_by(Analysis.created_at.desc())))


def get_analysis(db: Session, analysis_id: str) -> Analysis | None:
    return db.get(Analysis, analysis_id)


def create_analysis(db: Session, workspace: Workspace, user_id: str,
                    name: str, dataset_id: str, kind: str, hypothesis: str,
                    config: dict) -> Analysis:
    natural_key = f"{workspace.id}:{name}:{kind}"
    existing = db.scalar(select(Analysis).where(Analysis.natural_key == natural_key))
    if existing:
        return existing
    item = Analysis(
        natural_key=natural_key,
        name=name,
        kind=kind,
        hypothesis=hypothesis,
        config=config,
        dataset_id=dataset_id,
        workspace_id=workspace.id,
        created_by=user_id,
        status="ready",
    )
    db.add(item)
    db.flush()
    return item
