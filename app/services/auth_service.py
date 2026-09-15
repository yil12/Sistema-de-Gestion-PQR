from datetime import datetime, timedelta, timezone

import jwt
from app.core.config import settings
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.core.security import verify_password
from app.repositories.agente_repository import get_agente_by_email
from app.schemas.auth import LoginRequest


def create_access_token(data: dict) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def login_service(
    db: Session,
    data: LoginRequest,
) -> str:

    agente = get_agente_by_email(
        db,
        data.email,
    )

    if agente is None:
        raise BusinessException(
            status_code=401,
            detail="Credenciales inválidas.",
        )

    if not verify_password(
        data.password,
        agente.password_hash,
    ):
        raise BusinessException(
            status_code=401,
            detail="Credenciales inválidas.",
        )

    token = create_access_token(
        {
            "sub": str(agente.id),
            "rol_id": agente.rol_id,
        }
    )

    return token