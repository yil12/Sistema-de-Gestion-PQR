from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PQRCreate(BaseModel):
    solicitante_id: int
    tipo: str
    titulo: str
    descripcion: str
    categoria: str | None = None
    prioridad: str
    canal: str


class PQRResponse(BaseModel):
    id: int
    solicitante_id: int
    agente_asignado_id: int | None
    tipo: str
    titulo: str
    descripcion: str
    categoria: str | None
    prioridad: str
    estado: str
    canal: str
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)