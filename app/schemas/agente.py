from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class AgenteCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=150,
    )

    email: EmailStr

    rol_id: int = Field(
        gt=0,
    )

    password: str = Field(
        min_length=8,
        max_length=100,
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "El nombre no puede estar vacío."
            )

        return value


class AgenteResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )