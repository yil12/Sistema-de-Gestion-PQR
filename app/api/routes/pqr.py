from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.schemas.pqr import PQRCreate, PQRResponse
from app.services.pqr_service import register_pqr


router = APIRouter(
    prefix="/pqrs",
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
    response_model=PQRResponse,
    status_code=201,
    summary="Registrar una PQR",
)
def create_pqr(
    data: PQRCreate,
    db: Session = Depends(get_db),
):
    return register_pqr(db, data)