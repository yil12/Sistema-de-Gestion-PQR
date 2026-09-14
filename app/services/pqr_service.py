from sqlalchemy.orm import Session

from app.models.pqr import PQR
from app.repositories.pqr_repository import create_pqr
from app.schemas.pqr import PQRCreate
from app.utils.radicado import generar_radicado

from app.repositories.solicitante_repository import (
    get_solicitante_by_id,
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

