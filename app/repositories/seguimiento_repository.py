from sqlalchemy.orm import Session

from app.models.seguimiento import Seguimiento


def create_seguimiento(
    db: Session,
    seguimiento: Seguimiento,
) -> Seguimiento:
    db.add(seguimiento)
    db.flush()
    db.refresh(seguimiento)

    return seguimiento


def get_seguimientos_by_pqr(
    db: Session,
    pqr_id: int,
) -> list[Seguimiento]:
    return (
        db.query(Seguimiento)
        .filter(Seguimiento.pqr_id == pqr_id)
        .order_by(Seguimiento.fecha_registro.asc())
        .all()
    )

def create_escalamiento(
    db: Session,
    seguimiento: Seguimiento,
) -> Seguimiento:
    db.add(seguimiento)
    db.flush()
    db.refresh(seguimiento)

    return seguimiento