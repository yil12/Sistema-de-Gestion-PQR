from sqlalchemy.orm import Session

from app.models.pqr import PQR
from app.models.seguimiento import Seguimiento
from app.schemas.pqr import PQRCreate
from app.utils.radicado import generar_radicado

from app.repositories.solicitante_repository import (
    get_solicitante_by_id,
)

from app.repositories.seguimiento_repository import (
    create_seguimiento,
)

from app.repositories.pqr_repository import (
    create_pqr,
    get_pqr_by_id,
    get_pqr_by_radicado,
    get_pqrs,
    update_pqr_estado,
    assign_pqr_agent,
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

        seguimiento = Seguimiento(
            pqr_id=pqr.id,
            agente_id=None,
            tipo_accion="creada",
            descripcion="PQR creada correctamente.",
        )

        create_seguimiento(
            db=db,
            seguimiento=seguimiento,
        )

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


def get_pqrs_service(
    db: Session,
    estado: str | None = None,
    tipo: str | None = None,
    prioridad: str | None = None,
    categoria: str | None = None,
    page: int = 1,
    limit: int = 10,
) -> list[PQR]:
    return get_pqrs(
        db=db,
        estado=estado,
        tipo=tipo,
        prioridad=prioridad,
        categoria=categoria,
        page=page,
        limit=limit,
    )


def update_pqr_estado_service(
    db: Session,
    pqr_id: int,
    estado: str,
) -> PQR:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    try:
        pqr = update_pqr_estado(
            db=db,
            pqr=pqr,
            estado=estado,
        )

        db.commit()
        db.refresh(pqr)

        return pqr

    except Exception:
        db.rollback()
        raise


def assign_pqr_agent_service(
    db: Session,
    pqr_id: int,
    agente_id: int,
) -> PQR:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    try:
        agente_anterior_id = pqr.agente_asignado_id

        pqr = assign_pqr_agent(
            db=db,
            pqr=pqr,
            agente_id=agente_id,
        )

        if agente_anterior_id is None:
            tipo_accion = "asignacion"
            descripcion = (
                f"PQR asignada al agente {agente_id}."
            )
        else:
            tipo_accion = "reasignacion"
            descripcion = (
                f"PQR reasignada del agente "
                f"{agente_anterior_id} al agente {agente_id}."
            )

        seguimiento = Seguimiento(
            pqr_id=pqr_id,
            agente_id=agente_id,
            tipo_accion=tipo_accion,
            descripcion=descripcion,
        )

        create_seguimiento(
            db=db,
            seguimiento=seguimiento,
        )

        db.commit()
        db.refresh(pqr)

        return pqr

    except Exception:
        db.rollback()
        raise