from datetime import datetime


def generar_radicado(pqr_id: int) -> str:
    anio = datetime.now().year
    return f"PQR-{anio}-{pqr_id:06d}"