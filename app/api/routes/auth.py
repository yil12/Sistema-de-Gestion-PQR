from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.permission import get_current_agente
from app.schemas.auth import LoginRequest, TokenResponse, CurrentUserResponse
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


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_current_user(
    agente=Depends(get_current_agente),
):
    return CurrentUserResponse(
        id=agente.id,
        nombre=agente.nombre,
        email=agente.email,
        rol=agente.rol.nombre,
    )