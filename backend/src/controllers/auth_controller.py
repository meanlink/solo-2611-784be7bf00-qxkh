from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.schemas.auth import LoginRequest, TokenResponse, UserRead
from src.services.auth_service import authenticate


def login(db: Session, payload: LoginRequest) -> TokenResponse:
    result = authenticate(db, payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    return TokenResponse(access_token=result[1])


def current_user(user) -> UserRead:
    return UserRead(id=user.id, email=user.email, display_name=user.display_name, role=user.role)
