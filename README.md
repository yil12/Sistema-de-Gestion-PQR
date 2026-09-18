# Sistema de Gestión de PQR — Backend

API REST para la gestión de Peticiones, Quejas y Reclamos (PQR) de la Fundación Sersocial IPS.

El backend permite registrar, consultar y gestionar PQR, realizar seguimiento a las solicitudes y mantener la trazabilidad de su ciclo de vida.

El proyecto está desarrollado con **FastAPI**, **SQLAlchemy**, **Alembic** y **PostgreSQL**, utilizando Docker para facilitar la configuración del entorno de desarrollo y despliegue.

---

## Tabla de contenidos

* [Descripción](#-descripción)
* [Aplicación desplegada](#-aplicación-desplegada)
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
* [Despliegue](#-despliegue)
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
* Gestión de agentes internos.
* Asignación y escalamiento de PQR.
* Registro de respuestas y resoluciones.
* Persistencia de la información en PostgreSQL.
* Control de cambios del esquema mediante migraciones de Alembic.
* Autenticación mediante JWT y control de acceso basado en roles.

El sistema está diseñado con separación de responsabilidades para facilitar el mantenimiento y evolución del código.

---

# Aplicación desplegada

La aplicación se encuentra desplegada en Render para facilitar la evaluación del sistema.

### Frontend

```text
https://sistema-de-gestion-pqr-front-1.onrender.com
```

### Backend

```text
https://sistema-de-gestion-pqr-1.onrender.com
```

### Documentación Swagger

```text
https://sistema-de-gestion-pqr-1.onrender.com/docs
```

### Health Check

```text
https://sistema-de-gestion-pqr-1.onrender.com/health
```

El frontend consume la API del backend mediante la variable de entorno `VITE_API_URL`.

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
| Autenticación      | JWT               |
| Frontend           | React + Vite      |
| Despliegue         | Render            |

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

Durante el inicio del contenedor de la API se ejecutan automáticamente:

```text
1. Alembic → aplica las migraciones pendientes.
2. Seed    → carga los datos iniciales de prueba.
3. Uvicorn → inicia la API.
```

Por lo tanto, para una ejecución estándar no es necesario ejecutar manualmente las migraciones ni el seed después de levantar los contenedores.

### 4. Verificar la API

Una vez iniciados los contenedores, acceder a:

```text
http://localhost:8000/docs
```

La interfaz de Swagger permite consultar y probar los endpoints disponibles.

---

## Datos de prueba

El proyecto incluye un **seed idempotente** para facilitar la evaluación y permitir probar la aplicación con información inicial.

El seed crea o verifica:

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

> Estas credenciales corresponden exclusivamente a datos de prueba incluidos para facilitar la evaluación del sistema.

> El seed puede ejecutarse nuevamente sin generar duplicados de los datos principales de prueba.

Si se desea ejecutar manualmente:

```bash
docker compose exec api python -m app.seed
```

---

# Configuración de variables de entorno

El proyecto utiliza variables de entorno para configurar la conexión a PostgreSQL y otros parámetros de la aplicación.

Ejemplo:

```env
POSTGRES_DB=pqr_db
POSTGRES_USER=pqr_user
POSTGRES_PASSWORD=your_password
DATABASE_URL=postgresql+psycopg://pqr_user:your_password@db:5432/pqr_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
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

> Al utilizar el flujo estándar de Docker del proyecto, las migraciones se ejecutan automáticamente durante el inicio del contenedor de la API.

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

Local:

```text
http://localhost:8000/docs
```

Producción:

```text
https://sistema-de-gestion-pqr-1.onrender.com/docs
```

### ReDoc

Local:

```text
http://localhost:8000/redoc
```

Producción:

```text
https://sistema-de-gestion-pqr-1.onrender.com/redoc
```

---

# 🔌 Endpoints principales

## Autenticación

### Iniciar sesión

```http
POST /api/auth/login
```

Permite autenticar usuarios y obtener un token JWT.

### Consultar usuario autenticado

```http
GET /api/auth/me
```

Permite consultar la información del usuario autenticado.

---

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

### Búsqueda pública por radicado

```http
GET /api/pqr/buscar-publica?radicado={radicado}
```

Permite consultar públicamente el estado y la información disponible de una PQR mediante su número de radicado.

### Estadísticas

```http
GET /api/pqr/estadisticas
```

Permite consultar información estadística relacionada con las PQR.

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

## Asignación

El sistema dispone de endpoints para:

* Consultar agentes.
* Asignar PQR.
* Reasignar PQR.
* Gestionar la asignación de solicitudes a agentes internos.

---

## Escalamiento

El sistema permite gestionar el escalamiento de PQR cuando una solicitud requiere intervención de un nivel superior.

---

## Resolución

El sistema dispone de funcionalidades para registrar y gestionar respuestas y resoluciones asociadas a las PQR.

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
│   ├── api/
│   │   └── routes/
│   │
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

### JWT

Se utiliza autenticación basada en tokens JWT para proteger los endpoints internos y permitir diferenciar los permisos de acuerdo con el rol del usuario autenticado.

### Arquitectura por capas

La separación entre rutas, validación/lógica de negocio y persistencia permite reducir el acoplamiento entre componentes y facilita el mantenimiento del sistema.

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

El desarrollo se realizó de forma incremental, comenzando con el análisis y diseño, seguido de la implementación del backend, persistencia, autenticación y frontend.

---

# Despliegue

El backend y frontend fueron desplegados en **Render**.

### Backend

```text
https://sistema-de-gestion-pqr-1.onrender.com
```

### Frontend

```text
https://sistema-de-gestion-pqr-front-1.onrender.com
```

### Backend

El backend utiliza un contenedor Docker.

Durante el inicio del servicio se ejecutan:

```text
alembic upgrade head
python -m app.seed
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Esto permite que el entorno desplegado pueda crear/actualizar el esquema y disponer de datos iniciales de prueba.

### Frontend

El frontend está desarrollado con React + Vite y se genera mediante:

```bash
npm install
npm run build
```

El resultado del build corresponde a la carpeta:

```text
dist/
```

La variable de entorno utilizada para conectar el frontend con el backend es:

```env
VITE_API_URL=https://sistema-de-gestion-pqr-1.onrender.com
```

### CORS

El backend permite solicitudes desde el frontend local y desde el frontend desplegado:

```text
http://localhost:5173
https://sistema-de-gestion-pqr-front-1.onrender.com
```

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
* Resolver dudas relacionadas con FastAPI, SQLAlchemy, Alembic, Docker, React y despliegue.

El código generado o sugerido mediante IA fue revisado, adaptado y validado durante el desarrollo del proyecto.

La responsabilidad sobre las decisiones técnicas, integración y funcionamiento final del sistema corresponde al desarrollador.

---

# Repositorios

### Backend

```text
https://github.com/yil12/Sistema-de-Gestion-PQR
```

### Frontend

```text
https://github.com/yil12/Sistema-de-gestion-PQR-Front
```

---

# 👨‍💻 Autor

**Yilber Enrique Molina Devoz**

Ingeniero de Sistemas
Cartagena, Colombia
