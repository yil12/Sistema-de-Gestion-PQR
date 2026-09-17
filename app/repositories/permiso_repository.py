from sqlalchemy.orm import Session

from app.models.permiso import Permiso
from app.models.rol_permiso import RolPermiso


def get_permisos_by_rol(
    db: Session,
    rol_id: int,
) -> list[Permiso]:
    return (
        db.query(Permiso)
        .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)
        .filter(RolPermiso.rol_id == rol_id)
        .order_by(Permiso.id.asc())
        .all()
    )