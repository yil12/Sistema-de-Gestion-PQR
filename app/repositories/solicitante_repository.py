from sqlalchemy.orm import Session

from app.models.solicitante import Solicitante


def create_solicitante(
    db: Session,
    solicitante: Solicitante,
) -> Solicitante:
    db.add(solicitante)
    db.flush()
    db.refresh(solicitante)

    return solicitante


def get_solicitante_by_id(
    db: Session,
    solicitante_id: int,
) -> Solicitante | None:
    return db.get(Solicitante, solicitante_id)


def get_solicitante_by_documento(
    db: Session,
    numero_documento: str,
) -> Solicitante | None:
    return (
        db.query(Solicitante)
        .filter(
            Solicitante.numero_documento == numero_documento
        )
        .first()
    )


def get_solicitante_by_email(
    db: Session,
    email: str,
) -> Solicitante | None:
    return (
        db.query(Solicitante)
        .filter(
            Solicitante.email == email
        )
        .first()
    )