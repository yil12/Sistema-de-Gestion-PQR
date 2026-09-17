from sqlalchemy.orm import Session

from app.models.pqr import PQR
from app.models.seguimiento import Seguimiento
from app.models.solicitante import Solicitante
from app.schemas.pqr import PQRCreate
from app.utils.radicado import generar_radicado

from app.repositories.solicitante_repository import (
    create_solicitante,
    get_solicitante_by_documento,
    get_solicitante_by_email,
)

from app.repositories.seguimiento_repository import (
    create_seguimiento,
)

from app.repositories.agente_repository import (
    get_agente_by_id,
)

from app.repositories.pqr_repository import (
    create_pqr,
    get_pqr_by_id,
    get_pqr_by_radicado,
    get_pqrs,
    get_pqr_statistics,
    update_pqr_estado,
    assign_pqr_agent,
    get_pqr_detail_by_id,
    get_pqr_public_by_radicado,
)

from app.core.exceptions import BusinessException


def register_pqr(db: Session, data: PQRCreate) -> PQR:
    try:
        solicitante = get_solicitante_by_documento(
            db=db,
            numero_documento=data.solicitante.numero_documento,
        )

        if solicitante is None:
            solicitante = get_solicitante_by_email(
                db=db,
                email=data.solicitante.email,
            )

        if solicitante is None:
            solicitante = create_solicitante(
                db=db,
                solicitante=Solicitante(
                    nombre=data.solicitante.nombre,
                    apellido=data.solicitante.apellido,
                    tipo_documento=data.solicitante.tipo_documento,
                    numero_documento=data.solicitante.numero_documento,
                    email=data.solicitante.email,
                    telefono=data.solicitante.telefono,
                ),
            )

        pqr = PQR(
            solicitante_id=solicitante.id,
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
    pqr = get_pqr_detail_by_id(db, pqr_id)

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


def get_pqr_public_by_radicado_service(
    db: Session,
    radicado: str,
) -> PQR:
    pqr = get_pqr_public_by_radicado(db, radicado)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="No se encontró una PQR con el número de radicado indicado.",
        )

    return {
        "radicado": pqr.radicado, 
        "tipo": pqr.tipo, 
        "titulo": pqr.titulo, 
        "descripcion": pqr.descripcion, 
        "categoria": pqr.categoria,
        "prioridad": pqr.prioridad, 
        "estado": pqr.estado, 
        "created_at": pqr.created_at, 
        "updated_at": pqr.updated_at, 
        "historial": 
            [ { 
                "id": seguimiento.id, 
               "tipo_accion": seguimiento.tipo_accion, 
               "descripcion": seguimiento.descripcion, 
               "fecha_registro": seguimiento.fecha_registro, 
               } 
               for seguimiento in pqr.seguimientos 
            ],
    }


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

    if estado == "resuelta":
        raise BusinessException(
            status_code=400,
            detail=(
                "La PQR debe resolverse mediante el registro "
                "de una respuesta final."
            ),
        )

    if estado == "cerrada" and pqr.estado != "resuelta":
        raise BusinessException(
            status_code=400,
            detail=(
                "La PQR solo puede cerrarse cuando "
                "se encuentra en estado resuelta."
            ),
        )

    try:
        estado_anterior = pqr.estado

        pqr = update_pqr_estado(
            db=db,
            pqr=pqr,
            estado=estado,
        )

        seguimiento = Seguimiento(
            pqr_id=pqr_id,
            agente_id=None,
            tipo_accion="cambio_estado",
            descripcion=(
                f"Estado cambiado de "
                f"{estado_anterior} a {estado}."
            ),
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

        agente_nuevo = get_agente_by_id(db, agente_id)
        nombre_agente_nuevo = agente_nuevo.nombre if agente_nuevo else f"#{agente_id}"

        if agente_anterior_id is None:
            tipo_accion = "asignacion"
            descripcion = f"PQR asignada al agente {nombre_agente_nuevo}."
        else:
            agente_anterior = get_agente_by_id(db, agente_anterior_id)
            nombre_agente_anterior = agente_anterior.nombre if agente_anterior else f"#{agente_anterior_id}"

            tipo_accion = "reasignacion"
            descripcion = (
                f"PQR reasignada del agente "
                f"{nombre_agente_anterior} al agente {nombre_agente_nuevo}."
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


def resolve_pqr_service(
    db: Session,
    pqr_id: int,
    agente_id: int | None,
    respuesta: str,
) -> PQR:
    pqr = get_pqr_by_id(db, pqr_id)

    if pqr is None:
        raise BusinessException(
            status_code=404,
            detail="La PQR indicada no existe.",
        )

    if pqr.estado == "cerrada":
        raise BusinessException(
            status_code=400,
            detail="La PQR ya se encuentra cerrada.",
        )

    try:
        seguimiento = Seguimiento(
            pqr_id=pqr_id,
            agente_id=agente_id,
            tipo_accion="respuesta",
            descripcion=respuesta,
        )

        create_seguimiento(
            db=db,
            seguimiento=seguimiento,
        )

        pqr = update_pqr_estado(
            db=db,
            pqr=pqr,
            estado="resuelta",
        )

        db.commit()
        db.refresh(pqr)

        return pqr

    except Exception:
        db.rollback()
        raise

def get_pqr_statistics_service(
    db: Session,
) -> dict:
    return get_pqr_statistics(db)