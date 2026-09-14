from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TipoPQR(str, Enum):
    PETICION = "peticion"
    QUEJA = "queja"
    RECLAMO = "reclamo"


class PrioridadPQR(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class CanalPQR(str, Enum):
    WEB = "web"
    EMAIL = "email"
    PRESENCIAL = "presencial"

class PQRCreate(BaseModel):
    solicitante_id: int

    tipo: TipoPQR

    titulo: str = Field(
        min_length=5,
        max_length=200,
    )

    descripcion: str = Field(
        min_length=10,
    )

    categoria: str | None = Field(
        default=None,
        max_length=100,
    )

    prioridad: PrioridadPQR

    canal: CanalPQR

    @field_validator("titulo", "descripcion")
    @classmethod
    def validar_texto_obligatorio(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El campo no puede estar vacío.")

        return value

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("La categoría no puede estar vacía.")

        return value


class PQRResponse(BaseModel):
    id: int
    radicado: str
    solicitante_id: int
    agente_asignado_id: int | None
    tipo: TipoPQR
    titulo: str
    descripcion: str
    categoria: str | None
    prioridad: PrioridadPQR
    estado: str
    canal: CanalPQR
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)