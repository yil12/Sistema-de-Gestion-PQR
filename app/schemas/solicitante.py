from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, EmailStr

class SolicitanteCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
    )

    apellido: str = Field(
        min_length=2,
        max_length=100,
    )

    tipo_documento: str | None = Field(
        default=None,
        max_length=30,
    )

    numero_documento: str = Field(
        min_length=5,
        max_length=50,
    )

    email: EmailStr 

    telefono: str | None = Field(
        default=None,
        max_length=30,
    )

    @field_validator(
        "nombre",
        "apellido",
        "numero_documento",
        "email",
    )
    @classmethod
    def validar_campos_obligatorios(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "El campo no puede estar vacío."
            )

        return value

    @field_validator("tipo_documento", "telefono")
    @classmethod
    def validar_campos_opcionales(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class SolicitanteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    tipo_documento: str | None
    numero_documento: str
    email: EmailStr
    telefono: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )