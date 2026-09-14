from sqlalchemy.orm import Session

from app.models.pqr import PQR


def create_pqr(db: Session, pqr: PQR) -> PQR:
    db.add(pqr)
    db.flush()
    db.refresh(pqr)

    return pqr


def get_pqr_by_id(
    db: Session,
    pqr_id: int,
) -> PQR | None:
    return db.get(PQR, pqr_id)


def get_pqr_by_radicado(
    db: Session,
    radicado: str,
) -> PQR | None:
    return (
        db.query(PQR)
        .filter(PQR.radicado == radicado)
        .first()
    )