from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Seguimiento(Base):
    __tablename__ = "seguimiento"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    pqr_id: Mapped[int] = mapped_column(
        ForeignKey("pqr.id"),
        nullable=False,
    )

    agente_id: Mapped[int | None] = mapped_column(
        ForeignKey("agente.id"),
        nullable=True,
    )

    tipo_accion: Mapped[str | None] = mapped_column(
        String(50),
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    pqr = relationship(
        "PQR",
        back_populates="seguimientos",
    )

    agente = relationship(
        "Agente",
        back_populates="seguimientos",
    )