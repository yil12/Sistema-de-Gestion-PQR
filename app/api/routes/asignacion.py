from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.permission import require_permission
from app.schemas.pqr import PQRAssignAgent, PQRResponse
from app.schemas.response import ApiResponse
from app.services.pqr_service import assign_pqr_agent_service


router = APIRouter(
    prefix="/api/pqr/{pqr_id}/asignar",
    tags=["Asignación"],
)


@router.patch(
    "",
    response_model=ApiResponse[PQRResponse],
    status_code=200,
    summary="Asignar o reasignar una PQR",
)
def asignar_pqr(
    pqr_id: int,
    data: PQRAssignAgent,
    db: Session = Depends(get_db),
    agente=Depends(require_permission("pqr.asignar")),
):
    pqr = assign_pqr_agent_service(
        db=db,
        pqr_id=pqr_id,
        agente_id=data.agente_id,
    )

    return ApiResponse(
        exito=True,
        mensaje="PQR asignada correctamente.",
        data=pqr,
    )