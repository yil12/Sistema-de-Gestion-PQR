from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
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


def get_pqr_detail_by_id(
    db: Session,
    pqr_id: int,
) -> PQR | None:
    return (
        db.query(PQR)
        .options(
            joinedload(PQR.solicitante),
            joinedload(PQR.agente_asignado),
        )
        .filter(PQR.id == pqr_id)
        .first()
    )


def get_pqr_by_radicado(
    db: Session,
    radicado: str,
) -> PQR | None:
    return (
        db.query(PQR)
        .filter(PQR.radicado == radicado)
        .first()
    )

def get_pqr_public_by_radicado( 
    db: Session, 
    radicado: str, 
) -> PQR | None:
   return ( 
       db.query(PQR) 
       .options( 
           joinedload(PQR.seguimientos) 
        ) 
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


def assign_pqr_agent(
    db: Session,
    pqr: PQR,
    agente_id: int,
) -> PQR:
    pqr.agente_asignado_id = agente_id
    pqr.updated_at = datetime.utcnow()

    db.flush()
    db.refresh(pqr)

    return pqr


def get_pqr_statistics(
    db: Session,
) -> dict:
    total = (
        db.query(func.count(PQR.id))
        .scalar()
    )

    estados = (
        db.query(
            PQR.estado,
            func.count(PQR.id),
        )
        .group_by(PQR.estado)
        .all()
    )

    tipos = (
        db.query(
            PQR.tipo,
            func.count(PQR.id),
        )
        .group_by(PQR.tipo)
        .all()
    )

    prioridades = (
        db.query(
            PQR.prioridad,
            func.count(PQR.id),
        )
        .group_by(PQR.prioridad)
        .all()
    )

    return {
        "total": total,
        "por_estado": {
            estado: cantidad
            for estado, cantidad in estados
        },
        "por_tipo": {
            tipo: cantidad
            for tipo, cantidad in tipos
        },
        "por_prioridad": {
            prioridad: cantidad
            for prioridad, cantidad in prioridades
        },
    }