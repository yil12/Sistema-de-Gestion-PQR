from sqlalchemy.orm import Session

from app.models.solicitante import Solicitante


def get_solicitante_by_id(
    db: Session,
    solicitante_id: int,
) -> Solicitante | None:
    return db.get(Solicitante, solicitante_id)