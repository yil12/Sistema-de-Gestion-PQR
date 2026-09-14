from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.core.security import hash_password
from app.models.agente import Agente
from app.repositories.agente_repository import (
    create_agente,
    get_agente_by_email,
    get_agente_by_id,
    get_agentes,
)
from app.models.rol import Rol
from app.schemas.agente import AgenteCreate


def register_agente(
    db: Session,
    data: AgenteCreate,
) -> Agente:

    agente_existente = get_agente_by_email(
        db,
        data.email,
    )

    if agente_existente is not None:
        raise BusinessException(
            status_code=409,
            detail="Ya existe un agente con el correo electrónico indicado.",
        )

    rol = db.get(Rol, data.rol_id)

    if rol is None:
        raise BusinessException(
            status_code=404,
            detail="El rol indicado no existe.",
        )

    try:
        agente = Agente(
            nombre=data.nombre,
            email=data.email,
            rol_id=data.rol_id,
            password_hash=hash_password(data.password),
        )

        agente = create_agente(
            db=db,
            agente=agente,
        )

        db.commit()
        db.refresh(agente)

        return agente

    except Exception:
        db.rollback()
        raise


def get_agente_by_id_service(
    db: Session,
    agente_id: int,
) -> Agente:

    agente = get_agente_by_id(
        db,
        agente_id,
    )

    if agente is None:
        raise BusinessException(
            status_code=404,
            detail="El agente indicado no existe.",
        )

    return agente


def get_agentes_service(
    db: Session,
) -> list[Agente]:

    return get_agentes(db)


def get_agente_by_email_service(
    db: Session,
    email: str,
) -> Agente:

    agente = get_agente_by_email(
        db,
        email,
    )

    if agente is None:
        raise BusinessException(
            status_code=404,
            detail="No existe un agente con el correo electrónico indicado.",
        )

    return agente