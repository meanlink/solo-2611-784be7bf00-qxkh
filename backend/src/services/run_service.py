import hashlib
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.analysis import Analysis
from src.models.analysis_run import AnalysisRun
from src.models.comment import Comment
from src.models.dataset import Dataset
from src.services.analysis_engine import run_algorithm


def list_runs(db: Session) -> list[AnalysisRun]:
    return list(db.scalars(select(AnalysisRun).order_by(AnalysisRun.created_at.desc())))


def get_run(db: Session, run_id: str) -> AnalysisRun | None:
    return db.get(AnalysisRun, run_id)


def execute_run(db: Session, analysis: Analysis, actor_id: str) -> AnalysisRun:
    dataset = db.get(Dataset, analysis.dataset_id)
    if not dataset:
        raise ValueError("关联数据资产不存在")
    serialized = json.dumps(dataset.rows, sort_keys=True, ensure_ascii=False).encode()
    checksum = hashlib.sha256(serialized).hexdigest()
    natural_key = f"{analysis.id}:{checksum[:12]}:{datetime.now(timezone.utc).timestamp():.6f}"
    run = AnalysisRun(
        natural_key=natural_key,
        status="running",
        analysis_id=analysis.id,
        created_by=actor_id,
        checksum=checksum,
        started_at=datetime.now(timezone.utc),
    )
    db.add(run)
    db.flush()
    try:
        result = run_algorithm(dataset.rows, analysis.config or {})
        run.result = result
        run.metrics = result.get("metrics", [])
        run.status = "completed"
        run.completed_at = datetime.now(timezone.utc)
        analysis.status = "completed"
    except Exception as exc:
        run.status = "failed"
        run.error_message = str(exc)
        run.result = {"headline": "运行失败", "narrative": str(exc),
                      "metrics": [], "series": [], "table": [],
                      "method": "error", "caveat": "请检查数据字段与算法参数后重试。"}
        run.metrics = []
        run.completed_at = datetime.now(timezone.utc)
        analysis.status = "failed"
    return run


def list_comments(db: Session, run_id: str) -> list[Comment]:
    return list(db.scalars(select(Comment).where(Comment.run_id == run_id).order_by(Comment.created_at)))
