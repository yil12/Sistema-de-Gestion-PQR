from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError
from app.core.exceptions import BusinessException, business_exception_handler, validation_exception_handler

from app.api.routes.pqr import router as pqr_router
from app.api.routes.seguimiento import router as seguimiento_router
from app.api.routes.asignacion import router as asignacion_router
from app.api.routes.escalamiento import router as escalamiento_router
from app.api.routes.resolucion import router as resolucion_router
from app.api.routes.solicitante import router as solicitante_router
from app.api.routes.agente import router as agente_router





app = FastAPI(
    title="Sistema PQR API",
    description=(
        "API REST para la gestión de Peticiones, Quejas, "
        "Reclamos y Sugerencias (PQR)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    BusinessException,
    business_exception_handler,
)

app.include_router(pqr_router)
app.include_router(seguimiento_router)
app.include_router(asignacion_router)
app.include_router(escalamiento_router)
app.include_router(resolucion_router)
app.include_router(solicitante_router)
app.include_router(agente_router)





@app.get(
    "/health",
    tags=["Health"],
    summary="Verificar disponibilidad de la API",
)
def health_check():
    return {
        "status": "ok",
        "service": "pqr-api",
    }