from fastapi import FastAPI

from app.api.routes.pqr import router as pqr_router


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

app.include_router(pqr_router)

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