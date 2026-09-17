from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Agente(Base):
    __tablename__ = "agente"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    rol_id: Mapped[int] = mapped_column(
        ForeignKey("rol.id"),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    rol = relationship(
        "Rol",
        back_populates="agentes",
    )

    pqrs_asignadas = relationship(
        "PQR",
        back_populates="agente_asignado",
    )

    seguimientos = relationship(
        "Seguimiento",
        back_populates="agente",
    )