from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password

from app.models.agente import Agente
from app.models.pqr import PQR
from app.models.rol import Rol
from app.models.seguimiento import Seguimiento
from app.models.solicitante import Solicitante

from app.utils.radicado import generar_radicado


# ============================================================
# DATOS DE PRUEBA
# ============================================================

PASSWORD_PRUEBA = "Admin123"

AGENTES_SEED = [
    {
        "nombre": "Administrador PQR",
        "email": "admin.pqr@test.com",
        "rol_id": 3,
    },
    {
        "nombre": "Supervisor PQR",
        "email": "supervisor.pqr@test.com",
        "rol_id": 2,
    },
    {
        "nombre": "Agente Operativo PQR",
        "email": "agente.pqr@test.com",
        "rol_id": 1,
    },
]

SOLICITANTE_SEED = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "tipo_documento": "CC",
    "numero_documento": "1000000001",
    "email": "juan.perez@test.com",
    "telefono": "3000000000",
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_rol(
    db,
    rol_id: int,
) -> Rol | None:

    return db.scalar(
        select(Rol).where(
            Rol.id == rol_id
        )
    )


def obtener_o_crear_agente(
    db,
    nombre: str,
    email: str,
    rol_id: int,
) -> Agente:

    agente = db.scalar(
        select(Agente).where(
            Agente.email == email
        )
    )

    if agente:
        return agente

    rol = obtener_rol(
        db,
        rol_id,
    )

    if rol is None:
        raise RuntimeError(
            f"No existe el rol con ID {rol_id}. "
            "Ejecuta primero: alembic upgrade head"
        )

    agente = Agente(
        nombre=nombre,
        email=email,
        rol_id=rol_id,
        password_hash=hash_password(
            PASSWORD_PRUEBA
        ),
    )

    db.add(agente)
    db.flush()

    return agente


def obtener_o_crear_solicitante(
    db,
) -> Solicitante:

    solicitante = db.scalar(
        select(Solicitante).where(
            Solicitante.numero_documento
            == SOLICITANTE_SEED["numero_documento"]
        )
    )

    if solicitante:
        return solicitante

    solicitante = Solicitante(
        nombre=SOLICITANTE_SEED["nombre"],
        apellido=SOLICITANTE_SEED["apellido"],
        tipo_documento=SOLICITANTE_SEED["tipo_documento"],
        numero_documento=SOLICITANTE_SEED["numero_documento"],
        email=SOLICITANTE_SEED["email"],
        telefono=SOLICITANTE_SEED["telefono"],
    )

    db.add(solicitante)
    db.flush()

    return solicitante


def obtener_o_crear_pqr(
    db,
    solicitante: Solicitante,
    agente: Agente,
) -> PQR:

    pqr = db.scalar(
        select(PQR).where(
            PQR.titulo == "PQR de prueba del sistema"
        )
    )

    if pqr:
        return pqr

    pqr = PQR(
        solicitante_id=solicitante.id,
        agente_asignado_id=agente.id,
        tipo="peticion",
        titulo="PQR de prueba del sistema",
        descripcion=(
            "Esta PQR fue creada automáticamente "
            "mediante el seed del sistema para facilitar "
            "las pruebas de la aplicación."
        ),
        categoria="General",
        prioridad="media",
        estado="recibida",
        canal="web",
    )

    db.add(pqr)
    db.flush()

    # Utilizar la misma función que utiliza
    # el servicio normal de creación de PQR.
    pqr.radicado = generar_radicado(
        pqr.id
    )

    return pqr


def crear_seguimiento_inicial(
    db,
    pqr: PQR,
) -> Seguimiento | None:

    seguimiento_existente = db.scalar(
        select(Seguimiento).where(
            Seguimiento.pqr_id == pqr.id,
            Seguimiento.tipo_accion == "creada",
        )
    )

    if seguimiento_existente:
        return seguimiento_existente

    seguimiento = Seguimiento(
        pqr_id=pqr.id,
        agente_id=None,
        tipo_accion="creada",
        descripcion="PQR creada correctamente.",
    )

    db.add(seguimiento)
    db.flush()

    return seguimiento


# ============================================================
# SEED PRINCIPAL
# ============================================================

def seed() -> None:

    db = SessionLocal()

    try:
        print("")
        print("=" * 60)
        print(" INICIANDO SEED DEL SISTEMA PQR")
        print("=" * 60)
        print("")

        # ----------------------------------------------------
        # 1. Verificar roles
        # ----------------------------------------------------

        print("1. Verificando roles...")

        roles_requeridos = {
            1: "agente",
            2: "supervisor",
            3: "admin",
        }

        for rol_id, nombre_esperado in roles_requeridos.items():

            rol = obtener_rol(
                db,
                rol_id,
            )

            if rol is None:
                raise RuntimeError(
                    f"No existe el rol '{nombre_esperado}' "
                    f"(ID {rol_id}). "
                    "Ejecuta primero las migraciones de Alembic."
                )

            print(
                f"   ✓ Rol {rol.id}: {rol.nombre}"
            )

        # ----------------------------------------------------
        # 2. Crear agentes
        # ----------------------------------------------------

        print("")
        print("2. Creando agentes de prueba...")

        agentes = {}

        for datos in AGENTES_SEED:

            agente = obtener_o_crear_agente(
                db=db,
                nombre=datos["nombre"],
                email=datos["email"],
                rol_id=datos["rol_id"],
            )

            agentes[datos["email"]] = agente

            print(
                f"   ✓ {agente.nombre} "
                f"({agente.email})"
            )

        # ----------------------------------------------------
        # 3. Crear solicitante
        # ----------------------------------------------------

        print("")
        print(
            "3. Creando solicitante de prueba..."
        )

        solicitante = obtener_o_crear_solicitante(
            db
        )

        print(
            f"   ✓ {solicitante.nombre} "
            f"{solicitante.apellido}"
        )

        # ----------------------------------------------------
        # 4. Crear PQR
        # ----------------------------------------------------

        print("")
        print("4. Creando PQR de prueba...")

        agente_admin = agentes[
            "admin.pqr@test.com"
        ]

        pqr = obtener_o_crear_pqr(
            db=db,
            solicitante=solicitante,
            agente=agente_admin,
        )

        print(
            f"   ✓ PQR ID: {pqr.id}"
        )

        print(
            f"   ✓ Radicado: {pqr.radicado}"
        )

        # ----------------------------------------------------
        # 5. Crear seguimiento inicial
        # ----------------------------------------------------

        print("")
        print(
            "5. Creando seguimiento inicial..."
        )

        seguimiento = crear_seguimiento_inicial(
            db=db,
            pqr=pqr,
        )

        if seguimiento:
            print(
                "   ✓ Seguimiento inicial creado."
            )
        else:
            print(
                "   ✓ El seguimiento inicial "
                "ya existía."
            )

        # ----------------------------------------------------
        # 6. Confirmar transacción
        # ----------------------------------------------------

        db.commit()

        print("")
        print("=" * 60)
        print(" SEED COMPLETADO CORRECTAMENTE")
        print("=" * 60)
        print("")

        print("CREDENCIALES DE PRUEBA")
        print("-" * 60)

        print(
            "Administrador : admin.pqr@test.com"
        )
        print(
            "Supervisor    : supervisor.pqr@test.com"
        )
        print(
            "Agente        : agente.pqr@test.com"
        )
        print(
            f"Contraseña    : {PASSWORD_PRUEBA}"
        )

        print("")
        print("DATOS DE PRUEBA")
        print("-" * 60)

        print(
            f"Solicitante   : "
            f"{solicitante.nombre} "
            f"{solicitante.apellido}"
        )

        print(
            f"Documento     : "
            f"{solicitante.numero_documento}"
        )

        print(
            f"Email         : "
            f"{solicitante.email}"
        )

        print(
            f"PQR ID        : {pqr.id}"
        )

        print(
            f"Radicado      : {pqr.radicado}"
        )

        print("")
        print(
            "Puedes utilizar estas credenciales "
            "en Swagger para obtener el token."
        )
        print("")

    except Exception as exc:

        db.rollback()

        print("")
        print("=" * 60)
        print(" ERROR EJECUTANDO EL SEED")
        print("=" * 60)
        print("")
        print(str(exc))
        print("")

        raise

    finally:
        db.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    seed()