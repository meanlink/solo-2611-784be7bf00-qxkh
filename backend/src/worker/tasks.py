from datetime import datetime, timezone
from pathlib import Path

from src.worker.celery_app import celery_app


@celery_app.task(name="src.worker.tasks.heartbeat")
def heartbeat():
    path = Path("/app/artifacts/worker-heartbeat.txt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")
    return {"project": "sensor-corr", "status": "alive"}
