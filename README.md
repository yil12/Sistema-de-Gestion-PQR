# Sistema de Gestión de PQR — Backend

API REST para la gestión de Peticiones, Quejas y Reclamos (PQR) de la Fundación Sersocial IPS.

El backend permite registrar, consultar y gestionar PQR, realizar seguimiento a las solicitudes y mantener la trazabilidad de su ciclo de vida.

El proyecto está desarrollado con **FastAPI**, **SQLAlchemy**, **Alembic** y **PostgreSQL**, utilizando Docker para facilitar la configuración del entorno de desarrollo.

---

## Tabla de contenidos

* [Descripción](#-descripción)
* [Arquitectura](#-arquitectura)
* [Stack tecnológico](#-stack-tecnológico)
* [Requisitos](#-requisitos)
* [Inicio rápido con Docker](#-inicio-rápido-con-docker)
* [Configuración de variables de entorno](#-configuración-de-variables-de-entorno)
* [Base de datos y migraciones](#-base-de-datos-y-migraciones)
* [Ejecución sin Docker](#-ejecución-sin-docker)
* [Documentación de la API](#-documentación-de-la-api)
* [Endpoints principales](#-endpoints-principales)
* [Flujo de estados de una PQR](#-flujo-de-estados-de-una-pqr)
* [Estructura del proyecto](#-estructura-del-proyecto)
* [Decisiones de arquitectura](#-decisiones-de-arquitectura)
* [Gestión del proyecto](#-gestión-del-proyecto)
* [Declaración de uso de IA](#-declaración-de-uso-de-ia)
* [Autor](#-autor)

---

## Descripción

El backend proporciona los servicios necesarios para gestionar el ciclo de vida de una PQR:

* Registro de peticiones, quejas y reclamos.
* Consulta de PQR.
* Búsqueda mediante número de radicado.
* Filtrado por tipo, estado, prioridad y categoría.
* Consulta del detalle de una PQR.
* Actualización del estado.
* Registro de seguimientos.
* Consulta del historial de seguimientos.
* Gestión de solicitantes.
* Asignación de agentes internos.
* Persistencia de la información en PostgreSQL.
* Control de cambios del esquema mediante migraciones de Alembic.

El sistema está diseñado con separación de responsabilidades para facilitar el mantenimiento y evolución del código.

---

## Arquitectura

El backend utiliza una arquitectura por capas:

```text
┌──────────────────────────────┐
│          API / Routes        │
│      Endpoints FastAPI       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Schemas / Services      │
│ Validación y lógica negocio  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Models / Repository     │
│       SQLAlchemy ORM         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         PostgreSQL           │
└──────────────────────────────┘
```

Esta separación permite mantener diferenciadas las responsabilidades relacionadas con HTTP, validación, lógica de negocio y persistencia.

---

## Stack tecnológico

| Componente         | Tecnología        |
| ------------------ | ----------------- |
| Lenguaje           | Python 3.12       |
| Framework          | FastAPI           |
| ORM                | SQLAlchemy 2.0    |
| Migraciones        | Alembic           |
| Base de datos      | PostgreSQL 16     |
| Servidor ASGI      | Uvicorn           |
| Contenedores       | Docker            |
| Orquestación local | Docker Compose    |
| Documentación API  | OpenAPI / Swagger |

---

## Requisitos

### Con Docker

Se requiere:

* Git
* Docker
* Docker Compose

No es necesario instalar Python ni PostgreSQL localmente cuando se utiliza Docker.

### Sin Docker

Se requiere:

* Python 3.12
* PostgreSQL 16
* pip
* Entorno virtual recomendado

---

# Inicio rápido con Docker

La ejecución mediante Docker es la forma recomendada para reproducir el entorno del backend.

### 1. Clonar el repositorio

```bash
git clone https://github.com/yil12/Sistema-de-Gestion-PQR.git
cd Sistema-de-Gestion-PQR
```

### 2. Crear el archivo de variables de entorno

Copiar el archivo de ejemplo:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Revisar los valores del archivo `.env` antes de iniciar la aplicación.

### 3. Construir y levantar los servicios

```bash
docker compose up --build
```

El proyecto utiliza los siguientes servicios:

```text
API         → localhost:8000
PostgreSQL  → localhost:5432
```

### 4. Ejecutar las migraciones

Con los servicios levantados:

```bash
docker compose exec api alembic upgrade head
```

Esto crea o actualiza las tablas de la base de datos de acuerdo con las migraciones disponibles.

### 5. Cargar datos de prueba

El proyecto incluye un **seed** para facilitar la evaluación y permitir probar la aplicación con información inicial.

Ejecutar:

```bash
docker compose exec api python -m app.seed
```

El seed crea datos de prueba para:

* Un administrador.
* Un supervisor.
* Un agente operativo.
* Un solicitante.
* Una PQR de prueba.
* Un seguimiento inicial asociado a la PQR.

Los roles y permisos son creados previamente mediante las migraciones de Alembic.

### Credenciales de prueba

| Rol           | Email                     | Contraseña |
| ------------- | ------------------------- | ---------- |
| Administrador | `admin.pqr@test.com`      | `Admin123` |
| Supervisor    | `supervisor.pqr@test.com` | `Admin123` |
| Agente        | `agente.pqr@test.com`     | `Admin123` |

> El seed puede ejecutarse nuevamente sin generar duplicados de los datos principales de prueba.

### 6. Verificar la API

Una vez iniciados los contenedores, acceder a:

```text
http://localhost:8000/docs
```

La interfaz de Swagger permite consultar y probar los endpoints disponibles.

---

# Configuración de variables de entorno

El proyecto utiliza variables de entorno para configurar la conexión a PostgreSQL y otros parámetros de la aplicación.

Ejemplo:

```env
POSTGRES_DB=pqr_db
POSTGRES_USER=pqr_user
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql://pqr_user:your_password@db:5432/pqr_db
```

> Los valores utilizados en producción no deben almacenarse directamente en el repositorio.

El archivo `.env` se encuentra excluido mediante `.gitignore`.

El archivo `.env.example` contiene la estructura necesaria para configurar el entorno local.

---

# Base de datos y migraciones

La aplicación utiliza **PostgreSQL 16** como sistema de gestión de base de datos.

La persistencia se implementa mediante **SQLAlchemy 2.0** y las modificaciones del esquema se administran con **Alembic**.

## Ejecutar migraciones

```bash
docker compose exec api alembic upgrade head
```

Esto aplica las migraciones disponibles sobre la base de datos.

## Crear una nueva migración

Cuando se modifican los modelos:

```bash
docker compose exec api alembic revision --autogenerate -m "descripcion del cambio"
```

Después de revisar la migración generada:

```bash
docker compose exec api alembic upgrade head
```

## Verificar el estado de las migraciones

```bash
docker compose exec api alembic current
```

---

# Ejecución sin Docker

Docker es el método recomendado, pero el proyecto también puede ejecutarse localmente instalando las dependencias.

### 1. Crear entorno virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crear el archivo:

```text
.env
```

utilizando `.env.example` como referencia.

La base de datos PostgreSQL debe estar disponible localmente.

### 4. Ejecutar migraciones

```bash
alembic upgrade head
```

### 5. Cargar datos de prueba

```bash
python -m app.seed
```

### 6. Iniciar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

---

# Documentación de la API

FastAPI genera automáticamente la documentación basada en OpenAPI.

### Swagger UI

```text
http://localhost:8000/docs
```

---

# 🔌 Endpoints principales

## PQR

### Registrar una PQR

```http
POST /api/pqr
```

Permite registrar una nueva petición, queja o reclamo.

### Consultar PQR

```http
GET /api/pqr
```

Permite consultar las PQR y aplicar filtros.

Filtros disponibles:

```text
tipo
estado
prioridad
categoria
```

### Consultar una PQR

```http
GET /api/pqr/{id}
```

Permite consultar la información detallada de una PQR.

### Actualizar estado

```http
PATCH /api/pqr/{id}/estado
```

Permite actualizar el estado de una PQR dentro de su ciclo de gestión.

### Buscar por radicado

```http
GET /api/pqr/buscar?radicado={radicado}
```

Permite localizar una PQR mediante su número de radicado.

---

## Seguimiento

### Registrar seguimiento

```http
POST /api/pqr/{id}/seguimiento
```

Permite registrar una actuación o actualización relacionada con una PQR.

### Consultar seguimientos

```http
GET /api/pqr/{id}/seguimiento
```

Permite consultar el historial de seguimientos asociados a una PQR.

---

# Flujo de estados de una PQR

El ciclo principal de una PQR contempla:

```text
┌───────────┐
│  Recibida │
└─────┬─────┘
      │
      ▼
┌─────────────┐
│ En gestión  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Resuelta   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Cerrada   │
└─────────────┘
```

El historial de seguimiento permite registrar las actuaciones realizadas durante la gestión de cada solicitud.

---

# Estructura del proyecto

```text
Sistema-de-Gestion-PQR/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── agente.py
│   │   ├── permiso.py
│   │   ├── pqr.py
│   │   ├── rol.py
│   │   ├── rol_permiso.py
│   │   ├── seguimiento.py
│   │   └── solicitante.py
│   │
│   ├── seed.py
│   └── main.py
│
├── test/
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Decisiones de arquitectura

### FastAPI

Se seleccionó FastAPI por su soporte para:

* APIs REST.
* Validación mediante Pydantic.
* Documentación automática basada en OpenAPI.
* Integración con Python moderno.
* Desarrollo de servicios backend de forma eficiente.

### PostgreSQL

Se seleccionó PostgreSQL como motor relacional por:

* Integridad referencial.
* Soporte para relaciones entre entidades.
* Robustez.
* Compatibilidad con SQLAlchemy.
* Adecuación para un sistema transaccional como la gestión de PQR.

### SQLAlchemy

Se utiliza como ORM para representar las entidades del dominio y gestionar la interacción con PostgreSQL.

### Alembic

Permite versionar los cambios realizados sobre el esquema de la base de datos y reproducirlos en diferentes entornos.

### Docker

Docker permite estandarizar el entorno de ejecución y reducir diferencias entre la máquina de desarrollo y otros entornos.

---

# Gestión del proyecto

El desarrollo del proyecto se gestionó mediante un tablero Kanban utilizando Jira.

El trabajo se organizó mediante:

* Épicas.
* Historias de usuario.
* Tareas técnicas.
* Estimaciones.
* Registro de trabajo.
* Seguimiento del progreso.

El desarrollo se realizó de forma incremental, comenzando con el análisis y diseño, seguido de la implementación del backend, persistencia y frontend.

---

# Declaración de uso de IA

Durante el desarrollo se utilizaron herramientas de Inteligencia Artificial como apoyo al proceso de desarrollo.

La IA fue utilizada principalmente para:

* Consultar conceptos técnicos.
* Analizar alternativas de implementación.
* Revisar código.
* Identificar posibles errores.
* Apoyar la generación y mejora de documentación.
* Proponer estructuras iniciales de código.
* Resolver dudas relacionadas con FastAPI, SQLAlchemy, Alembic y Docker.

El código generado o sugerido mediante IA fue revisado, adaptado y validado durante el desarrollo del proyecto.

La responsabilidad sobre las decisiones técnicas, integración y funcionamiento final del sistema corresponde al desarrollador.

---

# 👨‍💻 Autor

**Yilber Enrique Molina Devoz**

Ingeniero de Sistemas
Cartagena, Colombia

---

## 🔗 Repositorio

Backend:

```text
https://github.com/yil12/Sistema-de-Gestion-PQR
```

El frontend del sistema se encuentra desarrollado en un repositorio independiente.
