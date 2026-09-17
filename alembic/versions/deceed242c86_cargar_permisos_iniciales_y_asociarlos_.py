"""cargar roles, permisos iniciales y asociarlos

Revision ID: deceed242c86
Revises: d5f8611fec15
Create Date: 2026-09-15 01:01:56.105568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "deceed242c86"
down_revision: Union[str, Sequence[str], None] = "d5f8611fec15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # ============================================================
    # ROLES INICIALES
    # ============================================================

    rol_table = sa.table(
        "rol",
        sa.column("id", sa.Integer),
        sa.column("nombre", sa.String),
    )

    op.bulk_insert(
        rol_table,
        [
            {"nombre": "agente"},
            {"nombre": "supervisor"},
            {"nombre": "admin"},
        ],
    )

    # Obtener los IDs reales de los roles creados
    roles_db = {
        row["nombre"]: row["id"]
        for row in bind.execute(
            sa.text(
                """
                SELECT id, nombre
                FROM rol
                WHERE nombre IN ('agente', 'supervisor', 'admin')
                """
            )
        ).mappings()
    }

    # ============================================================
    # PERMISOS INICIALES
    # ============================================================

    permisos = [
        {
            "nombre": "pqr.consultar",
            "descripcion": "Consultar PQR.",
        },
        {
            "nombre": "pqr.crear",
            "descripcion": "Registrar nuevas PQR.",
        },
        {
            "nombre": "pqr.seguimiento",
            "descripcion": "Registrar seguimientos de una PQR.",
        },
        {
            "nombre": "pqr.cambiar_estado",
            "descripcion": "Cambiar el estado de una PQR.",
        },
        {
            "nombre": "pqr.asignar",
            "descripcion": "Asignar una PQR a un agente.",
        },
        {
            "nombre": "pqr.reasignar",
            "descripcion": "Reasignar una PQR a otro agente.",
        },
        {
            "nombre": "pqr.escalar",
            "descripcion": "Escalar una PQR.",
        },
        {
            "nombre": "pqr.resolver",
            "descripcion": "Registrar la respuesta final y resolver una PQR.",
        },
        {
            "nombre": "usuario.consultar",
            "descripcion": "Consultar usuarios internos.",
        },
        {
            "nombre": "usuario.crear",
            "descripcion": "Crear usuarios internos.",
        },
        {
            "nombre": "usuario.gestionar_roles",
            "descripcion": "Gestionar roles de usuarios internos.",
        },
    ]

    permiso_table = sa.table(
        "permiso",
        sa.column("id", sa.Integer),
        sa.column("nombre", sa.String),
        sa.column("descripcion", sa.Text),
    )

    op.bulk_insert(permiso_table, permisos)

    # Obtener los IDs reales de los permisos
    permisos_db = {
        row["nombre"]: row["id"]
        for row in bind.execute(
            sa.text(
                """
                SELECT id, nombre
                FROM permiso
                """
            )
        ).mappings()
    }

    # ============================================================
    # PERMISOS POR ROL
    # ============================================================

    permisos_agente = [
        "pqr.consultar",
        "pqr.seguimiento",
        "pqr.cambiar_estado",
        "pqr.resolver",
    ]

    permisos_supervisor = permisos_agente + [
        "pqr.asignar",
        "pqr.reasignar",
        "pqr.escalar",
    ]

    permisos_admin = permisos_supervisor + [
        "usuario.consultar",
        "usuario.crear",
        "usuario.gestionar_roles",
    ]

    # ============================================================
    # ASOCIACIONES ROL-PERMISO
    # ============================================================

    asociaciones = []

    for nombre in permisos_agente:
        asociaciones.append(
            {
                "rol_id": roles_db["agente"],
                "permiso_id": permisos_db[nombre],
            }
        )

    for nombre in permisos_supervisor:
        asociaciones.append(
            {
                "rol_id": roles_db["supervisor"],
                "permiso_id": permisos_db[nombre],
            }
        )

    for nombre in permisos_admin:
        asociaciones.append(
            {
                "rol_id": roles_db["admin"],
                "permiso_id": permisos_db[nombre],
            }
        )

    rol_permiso_table = sa.table(
        "rol_permiso",
        sa.column("rol_id", sa.Integer),
        sa.column("permiso_id", sa.Integer),
    )

    op.bulk_insert(
        rol_permiso_table,
        asociaciones,
    )


def downgrade() -> None:
    bind = op.get_bind()

    # Eliminar primero las relaciones
    bind.execute(
        sa.text("DELETE FROM rol_permiso")
    )

    # Luego los permisos
    bind.execute(
        sa.text("DELETE FROM permiso")
    )

    # Finalmente los roles creados por esta migración
    bind.execute(
        sa.text(
            """
            DELETE FROM rol
            WHERE nombre IN ('agente', 'supervisor', 'admin')
            """
        )
    )