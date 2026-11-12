import argparse
import time

from sqlalchemy import select

from scripts.demo_data import demo_rows
from src.config import settings
from src.database import Base, SessionLocal, engine
from src.models.analysis import Analysis
from src.models.analysis_run import AnalysisRun
from src.models.audit_log import AuditLog
from src.models.comment import Comment
from src.models.dataset import Dataset
from src.models.user import User
from src.models.workspace import Workspace
from src.services.run_service import execute_run
from src.utils.security import hash_password


ACCOUNTS = [
    ("admin@batchdemo.dev", "演示管理员", "admin"),
    ("analyst@batchdemo.dev", "演示分析员", "analyst"),
    ("reviewer@batchdemo.dev", "演示复核员", "reviewer"),
]
PASSWORD = "Demo123!"


def wait_for_database(attempts=30):
    for index in range(attempts):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as exc:
            if index == attempts - 1:
                raise
            print(f"database not ready: {exc}", flush=True)
            time.sleep(2)


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        users = {}
        for email, display_name, role in ACCOUNTS:
            user = db.scalar(select(User).where(User.email == email))
            if not user:
                user = User(email=email, display_name=display_name, role=role,
                            password_hash=hash_password(PASSWORD))
                db.add(user)
                db.flush()
            users[role] = user

        admin = users["admin"]
        analyst = users["analyst"]
        reviewer = users["reviewer"]
        workspace = db.scalar(select(Workspace).where(Workspace.natural_key == "demo-workspace"))
        if not workspace:
            workspace = Workspace(
                natural_key="demo-workspace",
                name="冷链传感器相关室",
                client_name="沧澜冷链（18 座区域仓）",
                context_note="药品冷链仓同时采集温度、湿度、门磁和压缩机振动，运维希望定位彼此相关且值得现场排查的传感组合。",
                owner_id=admin.id,
            )
            db.add(workspace)
            db.flush()

        rows = demo_rows()
        chunk_size = max(len(rows) // 3, 1)
        datasets = []
        names = [
            "传感片段基线",
            "传感片段复核样本",
            "传感片段历史快照",
        ]
        sources = ["业务导出 CSV", "实验室复核 JSONL", "历史归档"]
        for index in range(3):
            subset = rows[index * chunk_size:(index + 1) * chunk_size] if index < 2 else rows[2 * chunk_size:]
            natural_key = f"demo-dataset-{index}"
            dataset = db.scalar(select(Dataset).where(Dataset.natural_key == natural_key))
            if not dataset:
                import hashlib
                import json
                raw = json.dumps(subset, sort_keys=True, ensure_ascii=False).encode()
                dataset = Dataset(
                    natural_key=natural_key,
                    name=names[index],
                    source=sources[index],
                    description=f"围绕{workspace.name}的{names[index]}，生成 seed 固定可复现。",
                    rows=subset,
                    row_count=len(subset),
                    checksum=hashlib.sha256(raw).hexdigest(),
                    workspace_id=workspace.id,
                    created_by=analyst.id,
                    status="ready",
                )
                db.add(dataset)
                db.flush()
            datasets.append(dataset)

        analyses = []
        definitions = [
            ("Pearson 与 Spearman 双相关分析", "primary", "比较核心业务指标，并给出效应量与不确定性。"),
            ("Benjamini-Hochberg 多重检验校正", "secondary", "用第二种口径复核主方案结论，检查敏感性与边界。"),
            ("相关方案稳健性方案", "primary", "按资产维度拆分，检查结论是否由单一分组驱动。"),
            ("审计记录复核方案", "secondary", "面向业务复核，保留算法口径与已知限制。"),
        ]
        for index, (name, kind, hypothesis) in enumerate(definitions):
            natural_key = f"seed-analysis-{index}"
            item = db.scalar(select(Analysis).where(Analysis.natural_key == natural_key))
            if not item:
                item = Analysis(
                    natural_key=natural_key,
                    name=name,
                    kind=kind,
                    status="ready",
                    hypothesis=hypothesis,
                    config={"seed": True, "variant": index + 1},
                    dataset_id=datasets[0].id,
                    workspace_id=workspace.id,
                    created_by=analyst.id,
                )
                db.add(item)
                db.flush()
            analyses.append(item)

        runs = []
        for index, analysis in enumerate(analyses[:3]):
            natural_key = f"seed-run-{index}"
            run = db.scalar(select(AnalysisRun).where(AnalysisRun.natural_key == natural_key))
            if not run:
                run = execute_run(db, analysis, analyst.id)
                run.natural_key = natural_key
                db.flush()
            runs.append(run)

        if not db.scalar(select(Comment).where(Comment.natural_key == "seed-comment-0")):
            db.add(Comment(natural_key="seed-comment-0",
                           body="请补充样本分群后的敏感性说明。",
                           decision="changes_requested", run_id=runs[0].id,
                           author_id=reviewer.id))
        if not db.scalar(select(Comment).where(Comment.natural_key == "seed-comment-1")):
            db.add(Comment(natural_key="seed-comment-1",
                           body="主口径已复核，可在周会发布。",
                           decision="approved", run_id=runs[1].id,
                           author_id=reviewer.id))
        if not db.scalar(select(AuditLog).where(AuditLog.action == "seed.bootstrap")):
            db.add(AuditLog(action="seed.bootstrap", resource_type="workspace",
                            resource_id=workspace.id, actor_id=admin.id,
                            detail={"datasets": len(datasets), "analyses": len(analyses),
                                     "project": "sensor-corr"}))
        db.commit()
        print(f"seed complete: users=3 datasets={len(datasets)} analyses={len(analyses)} runs={len(runs)}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait", action="store_true")
    args = parser.parse_args()
    if args.wait:
        wait_for_database()
    seed()


if __name__ == "__main__":
    main()
