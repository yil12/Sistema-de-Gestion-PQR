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


class TipoAccionSeguimiento(str, Enum):
    CREADA = "creada"
    COMENTARIO = "comentario"
    RESPUESTA = "respuesta"
    ESCALAMIENTO = "escalamiento"
    CAMBIO_ESTADO = "cambio_estado"
    ASIGNACION = "asignacion"
    REASIGNACION = "reasignacion"

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


class PQRFilterParams(BaseModel):
    estado: str | None = None
    tipo: TipoPQR | None = None
    prioridad: PrioridadPQR | None = None
    categoria: str | None = Field(
        default=None,
        max_length=100,
    )

    page: int = Field(
        default=1,
        ge=1,
    )

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    @field_validator("estado", "categoria")
    @classmethod
    def validar_filtros_texto(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class PQRUpdateEstado(BaseModel):
    estado: str = Field(
        min_length=1,
        max_length=30,
    )

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El estado no puede estar vacío.")

        estados_permitidos = {
            "recibida",
            "en_gestion",
            "resuelta",
            "cerrada",
        }

        if value not in estados_permitidos:
            raise ValueError(
                "El estado debe ser uno de: "
                "recibida, en_gestion, resuelta, cerrada."
            )

        return value


class SeguimientoCreate(BaseModel):
    agente_id: int | None = None

    tipo_accion: TipoAccionSeguimiento

    descripcion: str = Field(
        min_length=5,
    )

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "La descripción no puede estar vacía."
            )

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


class SeguimientoResponse(BaseModel):
    id: int
    pqr_id: int
    agente_id: int | None
    tipo_accion: TipoAccionSeguimiento
    descripcion: str
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)

class PQRAssignAgent(BaseModel):
    agente_id: int = Field(gt=0)
