from sqlalchemy.orm import Session

from app.models.pqr import PQR
from app.schemas.pqr import PQRCreate
from app.utils.radicado import generar_radicado

from app.repositories.solicitante_repository import (
    get_solicitante_by_id,
)

from app.repositories.pqr_repository import (
    create_pqr,
    get_pqr_by_id,
    get_pqr_by_radicado,
)

from app.core.exceptions import BusinessException


def register_pqr(db: Session, data: PQRCreate) -> PQR:
    solicitante = get_solicitante_by_id(
        db,
        data.solicitante_id,
    )

    if solicitante is None:
        raise BusinessException(
            status_code=404,
            detail="El solicitante indicado no existe.",
        )

    try:
        pqr = PQR(
            solicitante_id=data.solicitante_id,
            tipo=data.tipo,
            titulo=data.titulo,
            descripcion=data.descripcion,
            categoria=data.categoria,
            prioridad=data.prioridad,
            canal=data.canal,
        )

        pqr = create_pqr(db, pqr)

        pqr.radicado = generar_radicado(pqr.id)

        db.commit()
        db.refresh(pqr)

        return pqr

    except Exception:
        db.rollback()
        raise


def get_pqr_by_id_service(
    db: Session,
    pqr_id: int,
) -> PQR:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    return pqr


def get_pqr_by_radicado_service(
    db: Session,
    radicado: str,
) -> PQR:
    pqr = get_pqr_by_radicado(db, radicado)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="No existe una PQR asociada al radicado indicado.",
        )

    return pqr
