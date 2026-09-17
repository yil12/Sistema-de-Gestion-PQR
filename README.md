# Sistema de Gestión de PQR — Backend

API REST para la gestión de Peticiones, Quejas y Reclamos (PQR) de la Fundación Sersocial IPS.

El backend permite registrar, consultar y gestionar PQR, realizar seguimiento a las solicitudes y mantener la trazabilidad de su ciclo de vida.

El proyecto está desarrollado con **FastAPI**, **SQLAlchemy**, **Alembic** y **PostgreSQL**, utilizando Docker para facilitar la configuración del entorno de desarrollo.

---

##  Tabla de contenidos

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
* [Estructura del proyecto](#-estructura-del-proyecto)
* [Flujo de estados de una PQR](#-flujo-de-estados-de-una-pqr)
* [Pruebas](#-pruebas)
* [Decisiones de arquitectura](#-decisiones-de-arquitectura)
* [Gestión del proyecto](#-gestión-del-proyecto)
* [Declaración de uso de IA](#-declaración-de-uso-de-ia)
* [Autor](#-autor)

---

##  Descripción

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

##  Arquitectura

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

Esta separación permite mantener desacopladas las responsabilidades relacionadas con HTTP, lógica de negocio y persistencia.

---

##  Stack tecnológico

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

##  Requisitos

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

### 4. Verificar la API

Una vez iniciados los contenedores, acceder a:

```text
http://localhost:8000/docs
```

La interfaz de Swagger permite consultar y probar los endpoints disponibles.

---

#  Configuración de variables de entorno

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

Después de levantar el contenedor de la API, ejecutar:

```bash
docker compose exec api alembic upgrade head
```

Esto aplica las migraciones disponibles sobre la base de datos.

## Crear una nueva migración

Cuando se modifican los modelos:

```bash
docker compose exec api alembic revision --autogenerate -m "descripcion del cambio"
```

Después revisar la migración generada y aplicarla:

```bash
docker compose exec api alembic upgrade head
```

## Verificar el estado de las migraciones

```bash
docker compose exec api alembic current
```

---

#  Ejecución sin Docker

Docker es el método recomendado, pero el proyecto puede ejecutarse localmente instalando las dependencias.

### 1. Crear entorno virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

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

### 5. Iniciar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://localhost:8000
```

---

#  Documentación de la API

FastAPI genera automáticamente la documentación basada en OpenAPI.

### Swagger UI

```text
http://localhost:8000/docs
```

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

### Actualizar estado

```http
PATCH /api/pqr/{id}/estado
```

### Buscar por radicado

```http
GET /api/pqr/buscar?radicado={radicado}
```

---

## Seguimiento

### Registrar seguimiento

```http
POST /api/pqr/{id}/seguimiento
```

### Consultar seguimientos

```http
GET /api/pqr/{id}/seguimiento
```

---

#  Flujo de estados de una PQR

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

# 📁 Estructura del proyecto

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
│   │   ├── pqr.py
│   │   ├── rol.py
│   │   ├── seguimiento.py
│   │   └── solicitante.py
│   │
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

> La estructura puede ampliarse a medida que se incorporen nuevos módulos de la aplicación.

---


#  Decisiones de arquitectura

### FastAPI

Se seleccionó FastAPI por su soporte para:

* APIs REST.
* Validación mediante Pydantic.
* Documentación automática OpenAPI.
* Integración con Python moderno.
* Desarrollo rápido de servicios backend.

### PostgreSQL

Se seleccionó PostgreSQL como motor relacional por:

* Integridad referencial.
* Soporte para relaciones complejas.
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

El desarrollo se realizó de forma incremental, priorizando primero el análisis y diseño, seguido de la implementación del backend, persistencia y frontend.

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
* Resolver dudas relacionadas con FastAPI, SQLAlchemy, Alembic, Docker y React.

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
