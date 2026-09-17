from sqlalchemy.orm import Session

from app.models.agente import Agente


def create_agente(
    db: Session,
    agente: Agente,
) -> Agente:
    db.add(agente)
    db.flush()
    db.refresh(agente)

    return agente


def get_agente_by_id(
    db: Session,
    agente_id: int,
) -> Agente | None:
    return db.get(Agente, agente_id)


def get_agente_by_email(
    db: Session,
    email: str,
) -> Agente | None:
    return (
        db.query(Agente)
        .filter(
            Agente.email == email
        )
        .first()
    )


def get_agentes(
    db: Session,
) -> list[Agente]:
    return (
        db.query(Agente)
        .order_by(Agente.id.asc())
        .all()
    )