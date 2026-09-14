from sqlalchemy.orm import Session
from datetime import datetime

from app.models.pqr import PQR
from app.models.seguimiento import Seguimiento


def create_pqr(db: Session, pqr: PQR) -> PQR:
    db.add(pqr)
    db.flush()
    db.refresh(pqr)

    return pqr


def get_pqr_by_id(
    db: Session,
    pqr_id: int,
) -> PQR | None:
    return db.get(PQR, pqr_id)


def get_pqr_by_radicado(
    db: Session,
    radicado: str,
) -> PQR | None:
    return (
        db.query(PQR)
        .filter(PQR.radicado == radicado)
        .first()
    )


def get_pqrs(
    db: Session,
    estado: str | None = None,
    tipo: str | None = None,
    prioridad: str | None = None,
    categoria: str | None = None,
    page: int = 1,
    limit: int = 10,
) -> list[PQR]:
    query = db.query(PQR)

    if estado is not None:
        query = query.filter(PQR.estado == estado)

    if tipo is not None:
        query = query.filter(PQR.tipo == tipo)

    if prioridad is not None:
        query = query.filter(PQR.prioridad == prioridad)

    if categoria is not None:
        query = query.filter(PQR.categoria == categoria)

    offset = (page - 1) * limit

    return (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

def update_pqr_estado(
    db: Session,
    pqr: PQR,
    estado: str,
) -> PQR:
    pqr.estado = estado
    pqr.updated_at = datetime.utcnow()

    db.flush()
    db.refresh(pqr)

    return pqr
