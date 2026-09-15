from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import jwt

from app.core.config import settings
from app.core.database import get_db
from app.repositories.agente_repository import get_agente_by_id
from app.repositories.permiso_repository import get_permisos_by_rol


security = HTTPBearer()


def get_current_agente(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
        )

    agente_id = payload.get("sub")

    if agente_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    try:
        agente_id = int(agente_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    agente = get_agente_by_id(db, agente_id)

    if agente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario autenticado no existe.",
        )

    return agente


def require_permission(permission_name: str):
    def permission_dependency(
        agente=Depends(get_current_agente),
        db: Session = Depends(get_db),
    ):
        permisos = get_permisos_by_rol(
            db=db,
            rol_id=agente.rol_id,
        )

        tiene_permiso = any(
            permiso.nombre == permission_name
            for permiso in permisos
        )

        if not tiene_permiso:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para realizar esta operación.",
            )

        return agente

    return permission_dependency