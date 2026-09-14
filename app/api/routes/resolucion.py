from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pqr import PQRResolve, PQRResponse
from app.schemas.response import ApiResponse
from app.services.pqr_service import resolve_pqr_service


router = APIRouter(
    prefix="/api/pqr/{pqr_id}/resolucion",
    tags=["Resolución"],
)


@router.post(
    "",
    response_model=ApiResponse[PQRResponse],
    status_code=200,
    summary="Resolver una PQR",
)
def resolver_pqr(
    pqr_id: int,
    data: PQRResolve,
    db: Session = Depends(get_db),
):
    pqr = resolve_pqr_service(
        db=db,
        pqr_id=pqr_id,
        agente_id=None,
        respuesta=data.respuesta,
    )

    return ApiResponse(
        exito=True,
        mensaje="PQR resuelta correctamente.",
        data=pqr,
    )