from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.models.solicitante import Solicitante
from app.repositories.solicitante_repository import (
    create_solicitante,
    get_solicitante_by_documento,
    get_solicitante_by_email,
    get_solicitante_by_id,
)
from app.schemas.solicitante import SolicitanteCreate


def register_solicitante(
    db: Session,
    data: SolicitanteCreate,
) -> Solicitante:

    solicitante_documento = get_solicitante_by_documento(
        db,
        data.numero_documento,
    )

    if solicitante_documento is not None:
        raise BusinessException(
            status_code=409,
            detail="Ya existe un solicitante con el número de documento indicado.",
        )

    solicitante_email = get_solicitante_by_email(
        db,
        data.email,
    )

    if solicitante_email is not None:
        raise BusinessException(
            status_code=409,
            detail="Ya existe un solicitante con el correo electrónico indicado.",
        )

    try:
        solicitante = Solicitante(
            nombre=data.nombre,
            apellido=data.apellido,
            tipo_documento=data.tipo_documento,
            numero_documento=data.numero_documento,
            email=data.email,
            telefono=data.telefono,
        )

        solicitante = create_solicitante(
            db=db,
            solicitante=solicitante,
        )

        db.commit()
        db.refresh(solicitante)

        return solicitante

    except Exception:
        db.rollback()
        raise


def get_solicitante_by_id_service(
    db: Session,
    solicitante_id: int,
) -> Solicitante:

    solicitante = get_solicitante_by_id(
        db,
        solicitante_id,
    )

    if solicitante is None:
        raise BusinessException(
            status_code=404,
            detail="El solicitante indicado no existe.",
        )

    return solicitante


def get_solicitante_by_email_service(
    db: Session,
    email: str,
) -> Solicitante:

    solicitante = get_solicitante_by_email(
        db,
        email,
    )

    if solicitante is None:
        raise BusinessException(
            status_code=404,
            detail="No existe un solicitante con el correo electrónico indicado.",
        )

    return solicitante


def get_solicitante_by_documento_service(
    db: Session,
    numero_documento: str,
) -> Solicitante:

    solicitante = get_solicitante_by_documento(
        db,
        numero_documento,
    )

    if solicitante is None:
        raise BusinessException(
            status_code=404,
            detail="No existe un solicitante con el número de documento indicado.",
        )

    return solicitante