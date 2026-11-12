from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.comment import Comment
from src.schemas.analysis_run import CommentCreate, RunList, RunRead
from src.schemas.comment import CommentRead
from src.services import analysis_service, audit_service, run_service


def list_items(db: Session) -> RunList:
    items = run_service.list_runs(db)
    return RunList(items=[RunRead.model_validate(item) for item in items], total=len(items))


def execute(db: Session, analysis_id: str, user) -> RunRead:
    analysis = analysis_service.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="分析方案不存在")
    try:
        item = run_service.execute_run(db, analysis, user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    audit_service.record(db, "analysis.run", "analysis_run", item.id, user.id,
                         {"status": item.status, "checksum": item.checksum})
    db.commit()
    db.refresh(item)
    return RunRead.model_validate(item)


def get_item(db: Session, run_id: str) -> RunRead:
    item = run_service.get_run(db, run_id)
    if not item:
        raise HTTPException(status_code=404, detail="运行记录不存在")
    return RunRead.model_validate(item)


def list_comments(db: Session, run_id: str) -> list[CommentRead]:
    return [CommentRead.model_validate(item) for item in run_service.list_comments(db, run_id)]


def create_comment(db: Session, run_id: str, payload: CommentCreate, user) -> CommentRead:
    run = run_service.get_run(db, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="运行记录不存在")
    item = Comment(
        natural_key=f"{run_id}:{user.id}:{payload.body[:40]}:{len(run_id)}",
        body=payload.body,
        decision=payload.decision,
        run_id=run_id,
        author_id=user.id,
    )
    db.add(item)
    audit_service.record(db, "run.comment", "analysis_run", run_id, user.id,
                         {"decision": payload.decision})
    db.commit()
    db.refresh(item)
    return CommentRead.model_validate(item)
