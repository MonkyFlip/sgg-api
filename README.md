# SGG-API - Sistema Gestor de Gimnasios

API REST desarrollada con **FastAPI** y **MySQL** utilizando **Arquitectura Limpia** para la gestión integral de gimnasios.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tecnologías](#-tecnologías)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Documentación API](#-documentación-api)
- [Testing](#-testing)
- [Despliegue](#-despliegue)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Contribuir](#-contribuir)

---

## Características

### Gestión de Usuarios
- ✅ CRUD completo de usuarios
- ✅ Sistema de roles (Super Admin, Admin, Entrenador, Cliente)
- ✅ Autenticación JWT
- ✅ Perfiles personalizados

### Membresías y Pagos
- ✅ Gestión de tipos de membresías
- ✅ Renovaciones automáticas
- ✅ Facturación electrónica
- ✅ Registro de pagos
- ✅ Venta de productos (suplementos, merchandising)

### Control de Acceso
- ✅ Registro de entradas/salidas
- ✅ Validación de membresías activas
- ✅ Historial de accesos

### Entrenamiento Personal
- ✅ Asignación de entrenadores a clientes
- ✅ Generación de rutinas personalizadas
- ✅ Planes alimenticios (dietas)
- ✅ Seguimiento de progreso físico

### Clases Grupales
- ✅ Gestión de clases y horarios
- ✅ Sistema de reservas
- ✅ Control de capacidad

### Inventario
- ✅ Control de equipamiento
- ✅ Alertas de mantenimiento
- ✅ Gestión de productos para venta

### Reportes y Estadísticas
- ✅ Dashboard de métricas
- ✅ Reportes de ingresos
- ✅ Estadísticas de asistencia
- ✅ Análisis de rendimiento

### Multi-Tenant
- ✅ Soporte para múltiples gimnasios
- ✅ Aislamiento completo de datos
- ✅ Panel independiente por gimnasio

---

## Arquitectura

Este proyecto utiliza **Clean Architecture (Arquitectura Limpia)** con las siguientes capas:

```
┌─────────────────────────────────────────┐
│        API Layer (FastAPI)              │  ← Endpoints REST
├─────────────────────────────────────────┤
│        Service Layer                     │  ← Lógica de negocio
├─────────────────────────────────────────┤
│        Repository Layer                  │  ← Acceso a datos
├─────────────────────────────────────────┤
│        Model Layer (SQLAlchemy)         │  ← ORM
└─────────────────────────────────────────┘
```

### Principios aplicados:
- **SOLID**
- **Dependency Injection**
- **Repository Pattern**
- **Service Pattern**
- **DTO Pattern (Schemas)**

Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) para más detalles.

---

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos
- **Alembic** - Migraciones de base de datos
- **MySQL** - Base de datos relacional

### Seguridad
- **JWT** - Autenticación basada en tokens
- **Bcrypt** - Hash de contraseñas
- **CORS** - Control de origen cruzado

### Utilidades
- **python-dotenv** - Variables de entorno
- **ReportLab** - Generación de PDFs
- **Pandas** - Procesamiento de datos

### Testing
- **pytest** - Framework de testing
- **pytest-asyncio** - Testing asíncrono
- **pytest-cov** - Cobertura de código

---

## 📦 Requisitos

- Python 3.11+
- MySQL 8.0+
- pip
- virtualenv (recomendado)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sgg-api.git
cd sgg-api
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 5. Crear base de datos

```bash
# Conectarse a MySQL
mysql -u root -p

# Crear base de datos
CREATE DATABASE sgg_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sgg_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON sgg_database.* TO 'sgg_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 6. Ejecutar migraciones

```bash
alembic upgrade head
```

### 7. Inicializar datos (opcional)

```bash
python scripts/seed_data.py
```

---

## ⚙️ Configuración

Edita el archivo `.env` con tus configuraciones:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=sgg_user
DB_PASSWORD=your_password
DB_NAME=sgg_database

# Security
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

Ver [.env.example](.env.example) para todas las opciones disponibles.

---

## 💻 Uso

### Iniciar servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

### Documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Usando Docker

```bash
# Construir y levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Detener servicios
docker-compose down
```

---

## 📚 Documentación API

### Autenticación

```bash
# Login
POST /api/v1/auth/login
{
  "email": "admin@gym.com",
  "password": "password123"
}

# Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Iniciar sesión |
| POST | `/api/v1/auth/register` | Registrar usuario |
| GET | `/api/v1/usuarios` | Listar usuarios |
| POST | `/api/v1/usuarios` | Crear usuario |
| GET | `/api/v1/usuarios/{id}` | Obtener usuario |
| PUT | `/api/v1/usuarios/{id}` | Actualizar usuario |
| DELETE | `/api/v1/usuarios/{id}` | Eliminar usuario |
| GET | `/api/v1/membresias` | Listar membresías |
| POST | `/api/v1/accesos` | Registrar acceso |
| GET | `/api/v1/clases` | Listar clases |
| POST | `/api/v1/reservas` | Crear reserva |

Ver documentación completa en `/docs` una vez iniciado el servidor.

---

## 🧪 Testing

### Ejecutar todos los tests

```bash
pytest
```

### Tests unitarios

```bash
pytest tests/unit
```

### Tests de integración

```bash
pytest tests/integration
```

### Cobertura de código

```bash
pytest --cov=app --cov-report=html
# Abrir htmlcov/index.html
```

---

## 🚢 Despliegue

### AWS / Azure / GCP

1. Configurar base de datos en la nube
2. Actualizar variables de entorno
3. Usar Docker o desplegar directamente
4. Configurar HTTPS con certificado SSL
5. Configurar dominio personalizado

### Heroku

```bash
heroku create sgg-api
heroku addons:create cleardb:ignite
git push heroku main
```

### Railway / Render

Ver guías específicas en [docs/deployment.md](docs/deployment.md)

---

## 📁 Estructura del Proyecto

```
sgg-api/
├── app/
│   ├── api/              # Endpoints REST
│   ├── core/             # Configuración
│   ├── domain/           # Lógica de dominio
│   ├── models/           # Modelos SQLAlchemy
│   ├── repositories/     # Acceso a datos
│   ├── schemas/          # Schemas Pydantic
│   ├── services/         # Lógica de negocio
│   └── main.py           # Punto de entrada
├── tests/                # Tests
├── alembic/              # Migraciones
├── docs/                 # Documentación
└── scripts/              # Scripts útiles
```

Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) para estructura detallada.

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Miguel Angel Hernández Cervantes** - *Desarrollo inicial* - [MonkyFlip](https://github.com/MonkyFlip)

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM
- La comunidad de Python

---

## 📞 Contacto

¿Preguntas? Contáctanos en: miguelhercerv@gmail.com, miguelhercerv@outlook.com

---
