from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User
from src.utils.security import create_access_token, verify_password


def authenticate(db: Session, email: str, password: str) -> tuple[User, str] | None:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if not user or not user.is_active or not verify_password(password, user.password_hash):
        return None
    return user, create_access_token(user.id, user.role)
