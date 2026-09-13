from sqlalchemy.orm import Session

from app.models.pqr import PQR
from app.repositories.pqr_repository import create_pqr
from app.schemas.pqr import PQRCreate
from app.utils.radicado import generar_radicado


def register_pqr(db: Session, data: PQRCreate) -> PQR:
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