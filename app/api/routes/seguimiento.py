from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pqr import (
    SeguimientoCreate,
    SeguimientoResponse,
)
from app.schemas.response import ApiResponse
from app.services.seguimiento_service import (
    create_seguimiento_service,
    get_seguimientos_service,
)

router = APIRouter(
    prefix="/api/pqr/{pqr_id}/seguimiento",
    tags=["Seguimiento"],
)

@router.post(
    "",
    response_model=ApiResponse[SeguimientoResponse],
    status_code=201,
    summary="Registrar seguimiento de una PQR",
)
def registrar_seguimiento(
    pqr_id: int,
    data: SeguimientoCreate,
    db: Session = Depends(get_db),
):
    seguimiento = create_seguimiento_service(
        db=db,
        pqr_id=pqr_id,
        agente_id=data.agente_id,
        tipo_accion=data.tipo_accion,
        descripcion=data.descripcion,
    )

    return ApiResponse(
        exito=True,
        mensaje="Seguimiento registrado correctamente.",
        data=seguimiento,
    )


@router.get(
    "",
    response_model=ApiResponse[list[SeguimientoResponse]],
    status_code=200,
    summary="Consultar seguimientos de una PQR",
)
def listar_seguimientos(
    pqr_id: int,
    db: Session = Depends(get_db),
):
    seguimientos = get_seguimientos_service(
        db=db,
        pqr_id=pqr_id,
    )

    return ApiResponse(
        exito=True,
        mensaje="Seguimientos consultados correctamente.",
        data=seguimientos,
    )