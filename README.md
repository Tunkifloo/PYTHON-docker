# 🚀 Employees API - FastAPI + MySQL + Docker

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1.svg)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

API REST profesional para la gestión de empleados construida con **FastAPI**, **MySQL** y **Docker**. Implementa operaciones CRUD completas con validación de datos, paginación, búsqueda y documentación automática.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Patrones de Diseño](#-patrones-de-diseño)
- [Tecnologías](#️-tecnologías)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#️-instalación-y-configuración)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Testing](#-testing)
- [Documentación Interactiva](#-documentación-interactiva)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Características

- ✅ **CRUD Completo** de empleados (Create, Read, Update, Delete)
- ✅ **Validación automática** de datos con Pydantic
- ✅ **Documentación interactiva** con Swagger UI y ReDoc
- ✅ **Paginación** y búsqueda avanzada
- ✅ **Manejo de errores** personalizado
- ✅ **Base de datos MySQL** con SQLAlchemy ORM
- ✅ **Dockerización completa** con Docker Compose
- ✅ **Variables de entorno** para configuración
- ✅ **Health checks** para monitoreo
- ✅ **CORS** configurado para desarrollo

---

## 🏗️ Arquitectura

Este proyecto implementa una **arquitectura en capas (Layered Architecture)** que separa las responsabilidades y facilita el mantenimiento y escalabilidad:

```
┌─────────────────────────────────────────┐
│          API Layer (FastAPI)            │
│  - Endpoints REST                       │
│  - Validación de requests               │
│  - Serialización de responses           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Business Logic Layer              │
│  - Repositorios (Data Access)           │
│  - Lógica de negocio                    │
│  - Operaciones CRUD                     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Data Layer (SQLAlchemy)         │
│  - Modelos ORM                          │
│  - Conexión a base de datos             │
│  - Migraciones                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Database (MySQL 8.0)            │
│  - Almacenamiento persistente           │
│  - Índices y constraints                │
└─────────────────────────────────────────┘
```

### Flujo de Datos

1. **Request** → Cliente envía petición HTTP
2. **API Endpoint** → FastAPI recibe y valida con Pydantic schemas
3. **Repository** → Capa de acceso a datos ejecuta operaciones
4. **ORM** → SQLAlchemy traduce a SQL
5. **Database** → MySQL ejecuta query y retorna datos
6. **Response** → FastAPI serializa y envía respuesta al cliente

---

## 🎨 Patrones de Diseño

### 1. **Repository Pattern**
Abstrae la lógica de acceso a datos de la lógica de negocio:

```python
class EmployeeRepository:
    def get_all(self, skip: int, limit: int) -> List[Employee]
    def get_by_id(self, employee_id: int) -> Optional[Employee]
    def create(self, employee_data: EmployeeCreate) -> Employee
    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee
    def delete(self, employee_id: int) -> bool
```

**Beneficios:**
- Separa la lógica de acceso a datos
- Facilita el testing con mocks
- Permite cambiar el ORM sin afectar la API

### 2. **Dependency Injection**
FastAPI gestiona automáticamente las dependencias:

```python
def get_employees(db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    # ...
```

**Beneficios:**
- Código más testeable
- Gestión automática de recursos (conexiones DB)
- Inversión de control

### 3. **Data Transfer Objects (DTO)**
Schemas Pydantic para validación y serialización:

```python
EmployeeCreate    # Para crear empleados
EmployeeUpdate    # Para actualizar empleados
EmployeeResponse  # Para respuestas de la API
```

**Beneficios:**
- Validación automática de datos
- Documentación automática
- Type safety

### 4. **Configuration Management**
Centralización de configuración con Pydantic Settings:

```python
class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    # ...
```

**Beneficios:**
- Variables de entorno tipadas
- Validación de configuración al inicio
- Configuración centralizada

---

## 🛠️ Tecnologías

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.9+ | Lenguaje de programación |
| **FastAPI** | 0.115.0 | Framework web moderno y rápido |
| **Uvicorn** | 0.30.6 | Servidor ASGI de alto rendimiento |
| **SQLAlchemy** | 2.0.35 | ORM para Python |
| **PyMySQL** | 1.1.1 | Driver MySQL para Python |
| **Pydantic** | 2.9.2 | Validación de datos |
| **MySQL** | 8.0 | Base de datos relacional |
| **Docker** | Latest | Containerización |
| **Docker Compose** | Latest | Orquestación de contenedores |

---

## 📁 Estructura del Proyecto

```
PYTHON-docker/
├── app/
│   ├── __init__.py
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── config.py                    # Configuración y variables de entorno
│   ├── database.py                  # Configuración de SQLAlchemy
│   │
│   ├── api/                         # Capa de endpoints
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependencias compartidas
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── employees.py         # Endpoints de empleados
│   │
│   ├── models/                      # Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py
│   │   └── employee.py
│   │
│   ├── schemas/                     # Schemas Pydantic (DTOs)
│   │   ├── __init__.py
│   │   └── employee.py
│   │
│   └── repositories/                # Patrón Repository
│       ├── __init__.py
│       └── employee_repository.py
│
├── tests/                           # Tests unitarios y de integración
│   ├── __init__.py
│   └── test_employees.py
│
├── scripts/                         # Scripts de utilidad
│   └── init.sql                     # Script de inicialización DB
│
├── .env                             # Variables de entorno (no commitear)
├── .env.example                     # Ejemplo de variables de entorno
├── .gitignore                       # Archivos ignorados por Git
├── docker-compose.yml               # Orquestación Docker
├── Dockerfile                       # Imagen Docker de la aplicación
├── requirements.txt                 # Dependencias Python
└── README.md                        # Este archivo
```

### Descripción de Componentes

- **`app/main.py`**: Configuración de FastAPI, middlewares y rutas principales
- **`app/config.py`**: Gestión de variables de entorno con Pydantic Settings
- **`app/database.py`**: Configuración del engine y sesiones de SQLAlchemy
- **`app/models/`**: Definición de tablas usando SQLAlchemy ORM
- **`app/schemas/`**: Validación y serialización con Pydantic
- **`app/repositories/`**: Lógica de acceso a datos (patrón Repository)
- **`app/api/v1/`**: Endpoints REST versionados

---

## 📦 Requisitos Previos

Asegúrate de tener instalado:

- **Docker Desktop** (Windows/Mac) o **Docker Engine** (Linux)
  - [Descargar Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose** (incluido en Docker Desktop)
- **Git** para clonar el repositorio
- **(Opcional)** Python 3.9+ si deseas ejecutar localmente

### Verificar instalación:

```bash
docker --version
# Docker version 24.0.0 o superior

docker-compose --version
# Docker Compose version v2.20.0 o superior
```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/PYTHON-docker.git
cd PYTHON-docker
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Copiar el ejemplo
cp .env.example .env
```

Edita el archivo `.env`:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=3307
DATABASE_USER=admin
DATABASE_PASSWORD=admin123
DATABASE_NAME=employees_db

# Application Configuration
APP_NAME=Employees API
APP_VERSION=1.0.0
DEBUG=True
```

### 3. Construir y Levantar los Servicios

```bash
# Construir las imágenes
docker-compose build

# Levantar los contenedores
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

### 4. Verificar que los Servicios Estén Corriendo

```bash
# Ver el estado de los contenedores
docker-compose ps

# Deberías ver:
# NAME              STATUS              PORTS
# employees_mysql   Up (healthy)        0.0.0.0:3307->3306/tcp
# employees_api     Up                  0.0.0.0:8000->8000/tcp
```

### 5. Verificar la API

```bash
# Health check
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"healthy","service":"Employees API"}
```

### 6. Acceder a la Documentación

Abre tu navegador en:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔌 Endpoints de la API

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Endpoint raíz - información de la API |
| `GET` | `/health` | Health check - estado del servicio |
| `GET` | `/api/v1/employees/` | Obtener todos los empleados (con paginación) |
| `GET` | `/api/v1/employees/{id}` | Obtener un empleado por ID |
| `POST` | `/api/v1/employees/` | Crear un nuevo empleado |
| `PUT` | `/api/v1/employees/{id}` | Actualizar un empleado completo |
| `PATCH` | `/api/v1/employees/{id}` | Actualizar parcialmente un empleado |
| `DELETE` | `/api/v1/employees/{id}` | Eliminar un empleado |

---

## 📚 Ejemplos de Uso

### 1. Health Check

**Request:**
```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Employees API"
}
```

---

### 2. Crear un Empleado (CREATE)

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@company.com",
    "phone": "+51999999999",
    "position": "Software Developer",
    "department": "IT",
    "salary": 5000.00,
    "hire_date": "2024-01-15T00:00:00"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@company.com",
  "phone": "+51999999999",
  "position": "Software Developer",
  "department": "IT",
  "salary": 5000.0,
  "hire_date": "2024-01-15T00:00:00",
  "created_at": "2025-10-16T00:45:00.123456",
  "updated_at": "2025-10-16T00:45:00.123456"
}
```

---

### 3. Obtener Todos los Empleados (READ ALL)

**Request:**
```bash
# Sin parámetros
curl -X GET http://localhost:8000/api/v1/employees/

# Con paginación
curl -X GET "http://localhost:8000/api/v1/employees/?skip=0&limit=10"

# Con búsqueda
curl -X GET "http://localhost:8000/api/v1/employees/?search=Juan"
```

**Response (200 OK):**
```json
{
  "total": 1,
  "employees": [
    {
      "id": 1,
      "first_name": "Juan",
      "last_name": "Pérez",
      "email": "juan.perez@company.com",
      "phone": "+51999999999",
      "position": "Software Developer",
      "department": "IT",
      "salary": 5000.0,
      "hire_date": "2024-01-15T00:00:00",
      "created_at": "2025-10-16T00:45:00.123456",
      "updated_at": "2025-10-16T00:45:00.123456"
    }
  ],
  "page": 1,
  "page_size": 100
}
```

---

### 4. Obtener un Empleado por ID (READ ONE)

**Request:**
```bash
curl -X GET http://localhost:8000/api/v1/employees/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "first_name": "Juan",
  "last_name": "Pérez",
  "email": "juan.perez@company.com",
  "phone": "+51999999999",
  "position": "Software Developer",
  "department": "IT",
  "salary": 5000.0,
  "hire_date": "2024-01-15T00:00:00",
  "created_at": "2025-10-16T00:45:00.123456",
  "updated_at": "2025-10-16T00:45:00.123456"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Empleado con ID 999 no encontrado"
}
```

---

### 5. Actualizar un Empleado Completo (UPDATE)

**Request:**
```bash
curl -X PUT http://localhost:8000/api/v1/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Carlos",
    "last_name": "Pérez González",
    "email": "jc.perez@company.com",
    "phone": "+51988888888",
    "position": "Senior Software Developer",
    "department": "IT",
    "salary": 6500.00,
    "hire_date": "2024-01-15T00:00:00"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "first_name": "Juan Carlos",
  "last_name": "Pérez González",
  "email": "jc.perez@company.com",
  "phone": "+51988888888",
  "position": "Senior Software Developer",
  "department": "IT",
  "salary": 6500.0,
  "hire_date": "2024-01-15T00:00:00",
  "created_at": "2025-10-16T00:45:00.123456",
  "updated_at": "2025-10-16T00:50:00.789012"
}
```

---

### 6. Actualizar Parcialmente un Empleado (PATCH)

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/v1/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 7000.00,
    "position": "Tech Lead"
  }'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "first_name": "Juan Carlos",
  "last_name": "Pérez González",
  "email": "jc.perez@company.com",
  "phone": "+51988888888",
  "position": "Tech Lead",
  "department": "IT",
  "salary": 7000.0,
  "hire_date": "2024-01-15T00:00:00",
  "created_at": "2025-10-16T00:45:00.123456",
  "updated_at": "2025-10-16T00:55:00.456789"
}
```

---

### 7. Eliminar un Empleado (DELETE)

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/v1/employees/1
```

**Response (204 No Content):**
```
(Sin contenido en la respuesta)
```

**Error (404 Not Found):**
```json
{
  "detail": "Empleado con ID 999 no encontrado"
}
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Activar entorno virtual (si trabajas localmente)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=app --cov-report=html

# Ver reporte
open htmlcov/index.html
```

### Estructura de Tests

```python
# tests/test_employees.py
def test_create_employee():
    response = client.post("/api/v1/employees/", json={...})
    assert response.status_code == 201
    
def test_get_employees():
    response = client.get("/api/v1/employees/")
    assert response.status_code == 200
```

---

## 📖 Documentación Interactiva

FastAPI genera documentación automática e interactiva:

### Swagger UI
```
http://localhost:8000/docs
```
- Interfaz visual para probar endpoints
- Documentación generada automáticamente
- Try it out para ejecutar requests

### ReDoc
```
http://localhost:8000/redoc
```
- Documentación más limpia y profesional
- Ideal para presentaciones
- Mejor para lectura

---

## 🐛 Troubleshooting

### Problema: Puerto 3306 ya está en uso

**Error:**
```
bind: Only one usage of each socket address is normally permitted
```

**Solución:**
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "3307:3306"  # Usar 3307 externamente
```

---

### Problema: Contenedor FastAPI no inicia

**Diagnóstico:**
```bash
# Ver logs
docker logs employees_api

# Entrar al contenedor
docker exec -it employees_api bash
python -c "from app.main import app; print('OK')"
```

**Soluciones:**
- Verificar que todos los `__init__.py` existan
- Revisar `requirements.txt` para versiones compatibles
- Verificar que `.env` tenga todas las variables

---

### Problema: Error de conexión a MySQL

**Error:**
```
Can't connect to MySQL server on 'mysql'
```

**Solución:**
```bash
# Esperar a que MySQL esté ready
docker-compose down
docker-compose up -d

# Verificar health check
docker ps
```

---

### Problema: Limpiar y reiniciar todo

```bash
# Detener y eliminar contenedores, volúmenes y redes
docker-compose down -v

# Limpiar sistema Docker
docker system prune -a

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d
```

---

## 🚀 Comandos Útiles

### Docker Compose

```bash
# Construir servicios
docker-compose build

# Levantar servicios en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f fastapi

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar contenedores, volúmenes y redes
docker-compose down -v

# Reiniciar un servicio
docker-compose restart fastapi

# Ver estado de los servicios
docker-compose ps
```

### Docker

```bash
# Listar contenedores activos
docker ps

# Listar todos los contenedores
docker ps -a

# Ver logs de un contenedor
docker logs employees_api -f

# Ejecutar comando en contenedor
docker exec -it employees_api bash

# Detener un contenedor
docker stop employees_api

# Eliminar un contenedor
docker rm employees_api

# Eliminar todas las imágenes
docker image prune -a
```

### Base de Datos

```bash
# Conectarse a MySQL desde el contenedor
docker exec -it employees_mysql mysql -u admin -padmin123 employees_db

# Desde tu máquina (si tienes MySQL client)
mysql -h 127.0.0.1 -P 3307 -u admin -padmin123 employees_db

# Ver tablas
SHOW TABLES;

# Ver estructura de tabla
DESCRIBE employees;

# Ver datos
SELECT * FROM employees;
```

---

## 📝 Configuración para Producción

### Variables de Entorno

```env
# Production
DATABASE_HOST=production-db-host
DATABASE_PORT=3306
DATABASE_USER=prod_user
DATABASE_PASSWORD=secure_password_here
DATABASE_NAME=employees_prod_db

APP_NAME=Employees API
APP_VERSION=1.0.0
DEBUG=False  # Cambiar a False en producción
```

### Docker Compose para Producción

```yaml
# docker-compose.prod.yml
services:
  fastapi:
    restart: always
    environment:
      DEBUG: "False"
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

