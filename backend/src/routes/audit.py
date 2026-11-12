from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers import audit_controller
from src.database import get_db
from src.middlewares.auth import get_current_user
from src.schemas.audit_log import AuditList

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=AuditList)
def index(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return audit_controller.list_items(db)
