from celery import Celery
from src.config import settings

celery_app = Celery("batch_worker", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    beat_schedule={
        "write-heartbeat": {
            "task": "src.worker.tasks.heartbeat",
            "schedule": 45.0,
        }
    },
)
celery_app.autodiscover_tasks(["src.worker"])
