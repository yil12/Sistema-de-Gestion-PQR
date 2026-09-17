from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.permission import require_permission
from app.schemas.pqr import (
    PQREscalate,
    SeguimientoResponse,
)
from app.schemas.response import ApiResponse
from app.services.seguimiento_service import (
    create_escalamiento_service,
)

router = APIRouter(
    prefix="/api/pqr/{pqr_id}/escalar",
    tags=["Escalamiento"],
)


@router.post(
    "",
    response_model=ApiResponse[SeguimientoResponse],
    status_code=201,
    summary="Escalar una PQR",
)
def escalar_pqr(
    pqr_id: int,
    data: PQREscalate,
    db: Session = Depends(get_db),
    agente=Depends(require_permission("pqr.escalar")),
):
    seguimiento = create_escalamiento_service(
        db=db,
        pqr_id=pqr_id,
        destino=data.destino,
        descripcion=data.descripcion,
    )

    return ApiResponse(
        exito=True,
        mensaje="PQR escalada correctamente.",
        data=seguimiento,
    )