from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PQR(Base):
    __tablename__ = "pqr"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    solicitante_id: Mapped[int] = mapped_column(
        ForeignKey("solicitante.id"),
        nullable=False,
    )

    agente_asignado_id: Mapped[int | None] = mapped_column(
        ForeignKey("agente.id"),
        nullable=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    categoria: Mapped[str | None] = mapped_column(
        String(100),
    )

    prioridad: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="recibida",
    )

    canal: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    solicitante = relationship(
        "Solicitante",
        back_populates="pqrs",
    )

    agente_asignado = relationship(
        "Agente",
        back_populates="pqrs_asignadas",
    )

    seguimientos = relationship(
        "Seguimiento",
        back_populates="pqr",
    )