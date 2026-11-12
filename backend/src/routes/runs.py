from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers import run_controller
from src.database import get_db
from src.middlewares.auth import get_current_user, require_roles
from src.schemas.analysis_run import CommentCreate, RunList, RunRead
from src.schemas.comment import CommentRead

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("", response_model=RunList)
def index(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return run_controller.list_items(db)


@router.get("/{run_id}", response_model=RunRead)
def detail(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return run_controller.get_item(db, run_id)


@router.get("/{run_id}/comments", response_model=list[CommentRead])
def comments(run_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return run_controller.list_comments(db, run_id)


@router.post("/{run_id}/comments", response_model=CommentRead)
def comment(run_id: str, payload: CommentCreate, db: Session = Depends(get_db),
            user=Depends(require_roles("admin", "reviewer"))):
    return run_controller.create_comment(db, run_id, payload, user)
