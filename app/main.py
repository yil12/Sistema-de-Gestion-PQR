from fastapi import FastAPI


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