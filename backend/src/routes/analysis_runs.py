from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers import run_controller
from src.database import get_db
from src.middlewares.auth import require_roles
from src.schemas.analysis_run import RunRead

router = APIRouter(prefix="/analyses", tags=["analysis-runs"])


@router.post("/{analysis_id}/run", response_model=RunRead)
def execute(analysis_id: str, db: Session = Depends(get_db),
            user=Depends(require_roles("admin", "analyst"))):
    return run_controller.execute(db, analysis_id, user)
