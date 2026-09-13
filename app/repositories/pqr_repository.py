from sqlalchemy.orm import Session

from app.models.pqr import PQR


def create_pqr(db: Session, pqr: PQR) -> PQR:
    db.add(pqr)
    db.flush()
    db.refresh(pqr)

    return pqr