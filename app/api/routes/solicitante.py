from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.response import ApiResponse
from app.schemas.solicitante import (
    SolicitanteCreate,
    SolicitanteResponse,
)
from app.services.solicitante_service import (
    get_solicitante_by_id_service,
    get_solicitante_by_email_service,
    get_solicitante_by_documento_service,
    register_solicitante,
)


router = APIRouter(
    prefix="/api/solicitantes",
    tags=["Solicitantes"],
)


@router.post(
    "",
    response_model=ApiResponse[SolicitanteResponse],
    status_code=201,
    summary="Registrar un solicitante",
)
def registrar_solicitante(
    data: SolicitanteCreate,
    db: Session = Depends(get_db),
):
    solicitante = register_solicitante(
        db=db,
        data=data,
    )

    return ApiResponse(
        exito=True,
        mensaje="Solicitante registrado correctamente.",
        data=solicitante,
    )


@router.get(
    "/email/{email}",
    response_model=ApiResponse[SolicitanteResponse],
    status_code=200,
    summary="Consultar un solicitante por email",
)
def consultar_solicitante_por_email(
    email: str,
    db: Session = Depends(get_db),
):
    solicitante = get_solicitante_by_email_service(
        db=db,
        email=email,
    )

    return ApiResponse(
        exito=True,
        mensaje="Solicitante consultado correctamente.",
        data=solicitante,
    )


@router.get(
    "/documento/{numero_documento}",
    response_model=ApiResponse[SolicitanteResponse],
    status_code=200,
    summary="Consultar un solicitante por número de documento",
)
def consultar_solicitante_por_documento(
    numero_documento: str,
    db: Session = Depends(get_db),
):
    solicitante = get_solicitante_by_documento_service(
        db=db,
        numero_documento=numero_documento,
    )

    return ApiResponse(
        exito=True,
        mensaje="Solicitante consultado correctamente.",
        data=solicitante,
    )


@router.get(
    "/{solicitante_id}",
    response_model=ApiResponse[SolicitanteResponse],
    status_code=200,
    summary="Consultar un solicitante",
)
def consultar_solicitante(
    solicitante_id: int,
    db: Session = Depends(get_db),
):
    solicitante = get_solicitante_by_id_service(
        db=db,
        solicitante_id=solicitante_id,
    )

    return ApiResponse(
        exito=True,
        mensaje="Solicitante consultado correctamente.",
        data=solicitante,
    )