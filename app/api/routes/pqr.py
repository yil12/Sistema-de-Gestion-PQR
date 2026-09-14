from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.pqr import PQRCreate, PQRResponse
from app.schemas.response import ApiResponse
from app.services.pqr_service import register_pqr


router = APIRouter(
    prefix="/api/pqr",
    tags=["PQR"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


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