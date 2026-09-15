from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import login_service

router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticación"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    token = login_service(
        db=db,
        data=data,
    )

    return TokenResponse(
        access_token=token,
    )