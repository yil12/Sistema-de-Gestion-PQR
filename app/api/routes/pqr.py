from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.pqr import PQRCreate, PQRResponse
from app.schemas.response import ApiResponse
from app.services.pqr_service import (
    register_pqr,
    get_pqr_by_id_service,
    get_pqr_by_radicado_service,
)


router = APIRouter(
    prefix="/api/pqr",
    tags=["PQR"],
)


@router.post(
    "",
    response_model=ApiResponse[PQRResponse],
    status_code=201,
    summary="Registrar una PQR",
)
def create_pqr(
    data: PQRCreate,
    db: Session = Depends(get_db),
):
    pqr = register_pqr(db, data)

    return ApiResponse(
        exito=True,
        mensaje="PQR registrada correctamente.",
        data=pqr,
    )


@router.get(
    "/buscar",
    response_model=ApiResponse[PQRResponse],
    status_code=200,
    summary="Buscar una PQR por radicado",
)
def buscar_pqr_por_radicado(
    radicado: str,
    db: Session = Depends(get_db),
):
    pqr = get_pqr_by_radicado_service(
        db,
        radicado,
    )

    return ApiResponse(
        exito=True,
        mensaje="PQR encontrada correctamente.",
        data=pqr,
    )


@router.get(
    "/{pqr_id}",
    response_model=ApiResponse[PQRResponse],
    status_code=200,
    summary="Consultar una PQR por identificador",
)
def get_pqr(
    pqr_id: int,
    db: Session = Depends(get_db),
):
    pqr = get_pqr_by_id_service(
        db,
        pqr_id,
    )

    return ApiResponse(
        exito=True,
        mensaje="PQR consultada correctamente.",
        data=pqr,
    )