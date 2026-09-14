from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.agente import AgenteCreate, AgenteResponse
from app.services.agente_service import (
    get_agente_by_id_service,
    get_agentes_service,
    register_agente,
)

router = APIRouter(
    prefix="/api/agentes",
    tags=["Agentes"],
)


@router.post(
    "",
    response_model=AgenteResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_agente(
    data: AgenteCreate,
    db: Session = Depends(get_db),
):
    return register_agente(
        db=db,
        data=data,
    )


@router.get(
    "",
    response_model=list[AgenteResponse],
)
def listar_agentes(
    db: Session = Depends(get_db),
):
    return get_agentes_service(db)


@router.get(
    "/{agente_id}",
    response_model=AgenteResponse,
)
def obtener_agente(
    agente_id: int,
    db: Session = Depends(get_db),
):
    return get_agente_by_id_service(
        db=db,
        agente_id=agente_id,
    )