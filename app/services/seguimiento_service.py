from sqlalchemy.orm import Session

from app.core.exceptions import BusinessException
from app.models.seguimiento import Seguimiento
from app.repositories.pqr_repository import get_pqr_by_id
from app.repositories.seguimiento_repository import (
    create_seguimiento,
    get_seguimientos_by_pqr,
)


def create_seguimiento_service(
    db: Session,
    pqr_id: int,
    agente_id: int | None,
    tipo_accion: str,
    descripcion: str,
) -> Seguimiento:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    try:
        seguimiento = Seguimiento(
            pqr_id=pqr_id,
            agente_id=agente_id,
            tipo_accion=tipo_accion,
            descripcion=descripcion,
        )

        seguimiento = create_seguimiento(
            db,
            seguimiento,
        )

        db.commit()
        db.refresh(seguimiento)

        return seguimiento

    except Exception:
        db.rollback()
        raise


def get_seguimientos_service(
    db: Session,
    pqr_id: int,
) -> list[Seguimiento]:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    return get_seguimientos_by_pqr(
        db,
        pqr_id,
    )