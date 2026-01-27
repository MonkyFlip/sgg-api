# 🏋️ SGG-API - Sistema Gestor de Gimnasios
## Arquitectura Limpia con FastAPI + MySQL

---

## 📁 ESTRUCTURA COMPLETA DEL PROYECTO

```
sgg-api/
│
├── app/                                    # Aplicación principal
│   ├── __init__.py
│   ├── main.py                            # Punto de entrada de FastAPI
│   │
│   ├── api/                               # 🌐 Capa de Presentación (API REST)
│   │   ├── __init__.py
│   │   ├── dependencies.py                # Dependencias inyectables
│   │   │
│   │   └── v1/                            # API versión 1
│   │       ├── __init__.py
│   │       ├── router.py                  # Router principal v1
│   │       │
│   │       └── endpoints/                 # Endpoints REST
│   │           ├── __init__.py
│   │           ├── auth.py                # Autenticación y tokens
│   │           ├── gimnasios.py           # Gestión de gimnasios
│   │           ├── usuarios.py            # Gestión de usuarios
│   │           ├── roles.py               # Gestión de roles
│   │           ├── membresias.py          # Membresías y tipos
│   │           ├── accesos.py             # Control de acceso (entrada/salida)
│   │           ├── entrenadores.py        # Asignación entrenador-cliente
│   │           ├── clases.py              # Clases grupales
│   │           ├── reservas.py            # Reservas de clases
│   │           ├── productos.py           # Productos y categorías
│   │           ├── facturas.py            # Facturación
│   │           ├── pagos.py               # Registro de pagos
│   │           ├── inventario.py          # Equipamiento del gimnasio
│   │           ├── rutinas.py             # Rutinas de entrenamiento
│   │           ├── dietas.py              # Planes alimenticios
│   │           ├── progreso.py            # Seguimiento de progreso físico
│   │           ├── notificaciones.py      # Sistema de notificaciones
│   │           └── reportes.py            # Reportes y estadísticas
│   │
│   ├── core/                              # ⚙️ Configuración y Utilidades Core
│   │   ├── __init__.py
│   │   ├── config.py                      # Configuración de la aplicación
│   │   ├── database.py                    # Conexión y sesión de BD
│   │   ├── security.py                    # JWT, hashing, autenticación
│   │   ├── logging.py                     # Configuración de logs
│   │   └── constants.py                   # Constantes globales
│   │
│   ├── domain/                            # 🎯 Capa de Dominio (Lógica de Negocio)
│   │   ├── __init__.py
│   │   │
│   │   ├── entities/                      # Entidades de dominio (objetos de negocio)
│   │   │   ├── __init__.py
│   │   │   ├── gimnasio.py
│   │   │   ├── usuario.py
│   │   │   ├── membresia.py
│   │   │   ├── clase.py
│   │   │   ├── producto.py
│   │   │   ├── rutina.py
│   │   │   ├── dieta.py
│   │   │   └── factura.py
│   │   │
│   │   ├── exceptions/                    # Excepciones personalizadas
│   │   │   ├── __init__.py
│   │   │   ├── base.py                   # Excepción base
│   │   │   ├── auth_exceptions.py
│   │   │   ├── gimnasio_exceptions.py
│   │   │   ├── usuario_exceptions.py
│   │   │   ├── membresia_exceptions.py
│   │   │   └── validation_exceptions.py
│   │   │
│   │   ├── interfaces/                    # Interfaces (contratos)
│   │   │   ├── __init__.py
│   │   │   ├── repository_interface.py    # Interface genérica de repositorio
│   │   │   ├── usuario_repository_interface.py
│   │   │   ├── gimnasio_repository_interface.py
│   │   │   └── ...                       # Más interfaces según necesidad
│   │   │
│   │   └── enums/                         # Enumeraciones de dominio
│   │       ├── __init__.py
│   │       ├── rol_enum.py
│   │       ├── estado_membresia_enum.py
│   │       ├── genero_enum.py
│   │       ├── dia_semana_enum.py
│   │       ├── tipo_acceso_enum.py
│   │       └── estado_factura_enum.py
│   │
│   ├── schemas/                           # 📋 Schemas Pydantic (DTOs)
│   │   ├── __init__.py
│   │   ├── base.py                       # Schema base
│   │   ├── auth.py                       # Login, Token, Register
│   │   ├── gimnasio.py                   # GimnasioCreate, GimnasioUpdate, GimnasioResponse
│   │   ├── usuario.py                    # UsuarioCreate, UsuarioUpdate, UsuarioResponse
│   │   ├── rol.py
│   │   ├── membresia.py
│   │   ├── membresia_tipo.py
│   │   ├── acceso.py
│   │   ├── entrenador_cliente.py
│   │   ├── clase.py
│   │   ├── reserva.py
│   │   ├── producto.py
│   │   ├── producto_categoria.py
│   │   ├── factura.py
│   │   ├── pago.py
│   │   ├── inventario.py
│   │   ├── inventario_categoria.py
│   │   ├── rutina.py
│   │   ├── dieta.py
│   │   ├── progreso_fisico.py
│   │   ├── notificacion.py
│   │   └── pagination.py                 # Schema de paginación
│   │
│   ├── services/                          # 💼 Capa de Servicios (Casos de Uso)
│   │   ├── __init__.py
│   │   ├── base_service.py               # Servicio base
│   │   ├── auth_service.py               # Autenticación y autorización
│   │   ├── gimnasio_service.py           # Lógica de negocio de gimnasios
│   │   ├── usuario_service.py            # Lógica de negocio de usuarios
│   │   ├── rol_service.py
│   │   ├── membresia_service.py          # Renovaciones, cálculos, validaciones
│   │   ├── acceso_service.py             # Validación de acceso, registro entrada/salida
│   │   ├── entrenador_service.py         # Asignación, gestión de clientes
│   │   ├── clase_service.py
│   │   ├── reserva_service.py            # Validación de cupos, cancelaciones
│   │   ├── producto_service.py
│   │   ├── factura_service.py            # Generación de facturas, cálculos
│   │   ├── pago_service.py               # Registro y validación de pagos
│   │   ├── inventario_service.py         # Control de stock, alertas
│   │   ├── rutina_service.py             # Generación y asignación de rutinas
│   │   ├── dieta_service.py              # Generación y asignación de dietas
│   │   ├── progreso_service.py           # Análisis de progreso
│   │   ├── notificacion_service.py       # Envío de notificaciones
│   │   └── reporte_service.py            # Generación de reportes y estadísticas
│   │
│   ├── repositories/                      # 💾 Capa de Acceso a Datos
│   │   ├── __init__.py
│   │   ├── base_repository.py            # Repositorio base con operaciones CRUD
│   │   ├── gimnasio_repository.py        # Operaciones DB de gimnasios
│   │   ├── usuario_repository.py         # Operaciones DB de usuarios
│   │   ├── rol_repository.py
│   │   ├── membresia_repository.py
│   │   ├── membresia_tipo_repository.py
│   │   ├── acceso_repository.py
│   │   ├── entrenador_cliente_repository.py
│   │   ├── clase_repository.py
│   │   ├── reserva_repository.py
│   │   ├── producto_repository.py
│   │   ├── producto_categoria_repository.py
│   │   ├── factura_repository.py
│   │   ├── pago_repository.py
│   │   ├── inventario_repository.py
│   │   ├── inventario_categoria_repository.py
│   │   ├── rutina_repository.py
│   │   ├── dieta_repository.py
│   │   ├── progreso_fisico_repository.py
│   │   └── notificacion_repository.py
│   │
│   ├── models/                            # 🗄️ Modelos SQLAlchemy (ORM)
│   │   ├── __init__.py
│   │   ├── base.py                       # Modelo base
│   │   ├── gimnasio.py                   # Modelo de tabla gimnasios
│   │   ├── rol.py
│   │   ├── usuario.py
│   │   ├── membresia.py
│   │   ├── membresia_tipo.py
│   │   ├── acceso.py
│   │   ├── entrenador_cliente.py
│   │   ├── clase.py
│   │   ├── clase_horario.py
│   │   ├── reserva.py
│   │   ├── producto.py
│   │   ├── producto_categoria.py
│   │   ├── factura.py
│   │   ├── factura_detalle.py
│   │   ├── pago.py
│   │   ├── inventario.py
│   │   ├── inventario_categoria.py
│   │   ├── rutina.py
│   │   ├── rutina_ejercicio.py
│   │   ├── dieta.py
│   │   ├── dieta_comida.py
│   │   ├── progreso_fisico.py
│   │   ├── notificacion.py
│   │   └── log_actividad.py
│   │
│   ├── middleware/                        # 🔒 Middlewares
│   │   ├── __init__.py
│   │   ├── authentication.py             # Middleware de autenticación
│   │   ├── gym_context.py                # Middleware para contexto de gimnasio
│   │   ├── logging_middleware.py         # Logging de requests
│   │   ├── error_handler.py              # Manejo global de errores
│   │   └── rate_limiter.py               # Limitador de peticiones
│   │
│   └── utils/                             # 🛠️ Utilidades
│       ├── __init__.py
│       ├── date_utils.py                 # Utilidades de fechas
│       ├── validators.py                 # Validadores personalizados
│       ├── pagination.py                 # Utilidades de paginación
│       ├── file_handler.py               # Manejo de archivos
│       ├── email_sender.py               # Envío de emails
│       └── pdf_generator.py              # Generación de PDFs
│
├── tests/                                 # 🧪 Tests
│   ├── __init__.py
│   ├── conftest.py                       # Configuración de pytest
│   │
│   ├── unit/                             # Tests unitarios
│   │   ├── __init__.py
│   │   ├── services/                     # Tests de servicios
│   │   │   ├── test_usuario_service.py
│   │   │   ├── test_membresia_service.py
│   │   │   └── ...
│   │   ├── repositories/                 # Tests de repositorios
│   │   │   ├── test_usuario_repository.py
│   │   │   └── ...
│   │   └── api/                          # Tests de endpoints
│   │       ├── test_usuarios_endpoint.py
│   │       └── ...
│   │
│   ├── integration/                      # Tests de integración
│   │   ├── __init__.py
│   │   ├── test_usuario_flow.py
│   │   ├── test_membresia_flow.py
│   │   └── ...
│   │
│   └── e2e/                              # Tests end-to-end
│       ├── __init__.py
│       └── test_complete_flow.py
│
├── alembic/                               # 🔄 Migraciones de Base de Datos
│   ├── versions/                         # Carpeta de versiones de migración
│   │   └── .gitkeep
│   ├── env.py                            # Configuración de Alembic
│   ├── script.py.mako                    # Template de scripts
│   └── alembic.ini                       # Configuración de Alembic
│
├── docs/                                  # 📚 Documentación
│   ├── api/                              # Documentación de API
│   │   └── openapi.json
│   ├── architecture.md                   # Arquitectura del sistema
│   ├── database.md                       # Documentación de BD
│   └── deployment.md                     # Guía de despliegue
│
├── scripts/                               # 📜 Scripts útiles
│   ├── init_db.py                        # Inicializar BD con datos
│   ├── seed_data.py                      # Datos de prueba
│   └── migration_helper.py               # Ayudas para migraciones
│
├── .env.example                           # Ejemplo de variables de entorno
├── .env                                   # Variables de entorno (NO versionar)
├── .gitignore                            # Archivos ignorados por git
├── requirements.txt                       # Dependencias Python
├── requirements-dev.txt                   # Dependencias de desarrollo
├── Dockerfile                             # Dockerfile para contenedor
├── docker-compose.yml                     # Compose para desarrollo
├── pytest.ini                             # Configuración de pytest
├── setup.py                               # Setup del proyecto
└── README.md                              # Documentación principal
```

---

## 🎯 DESCRIPCIÓN DE CAPAS

### 1. **API Layer (app/api/)**
- **Responsabilidad**: Manejar requests HTTP, validación de entrada, respuestas HTTP
- **Tecnología**: FastAPI, Pydantic
- **No contiene**: Lógica de negocio
- **Dependencias**: Services, Schemas

### 2. **Service Layer (app/services/)**
- **Responsabilidad**: Lógica de negocio, casos de uso, coordinación
- **Contiene**: Validaciones de negocio, cálculos, orquestación
- **No contiene**: Queries SQL directas
- **Dependencias**: Repositories, Domain

### 3. **Repository Layer (app/repositories/)**
- **Responsabilidad**: Acceso a datos, queries, persistencia
- **Contiene**: Operaciones CRUD, queries complejas
- **No contiene**: Lógica de negocio
- **Dependencias**: Models (SQLAlchemy)

### 4. **Domain Layer (app/domain/)**
- **Responsabilidad**: Entidades de negocio, reglas de dominio
- **Contiene**: Entidades, excepciones, interfaces, enums
- **No contiene**: Dependencias externas
- **Dependencias**: Ninguna (capa más interna)

### 5. **Models Layer (app/models/)**
- **Responsabilidad**: Mapeo objeto-relacional
- **Tecnología**: SQLAlchemy
- **Contiene**: Definición de tablas y relaciones

### 6. **Schemas Layer (app/schemas/)**
- **Responsabilidad**: Validación y serialización de datos
- **Tecnología**: Pydantic
- **Contiene**: DTOs (Data Transfer Objects)

---

## 🔄 FLUJO DE UNA REQUEST

```
1. Request HTTP
   ↓
2. API Endpoint (FastAPI)
   ↓
3. Schema Validation (Pydantic)
   ↓
4. Service Layer (Lógica de negocio)
   ↓
5. Repository Layer (Acceso a datos)
   ↓
6. Model (SQLAlchemy)
   ↓
7. Database (MySQL)
   ↓
8. Response (JSON)
```

---

## 🛡️ PRINCIPIOS APLICADOS

### SOLID
- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Interfaces bien definidas
- **I**nterface Segregation: Interfaces específicas
- **D**ependency Inversion: Depende de abstracciones

### Clean Architecture
- **Independencia de frameworks**: La lógica no depende de FastAPI
- **Testeable**: Cada capa se puede testear independientemente
- **Independiente de UI**: API REST, GraphQL, gRPC, etc.
- **Independiente de BD**: Puedes cambiar MySQL por PostgreSQL
- **Independiente de agentes externos**: Servicios externos son plugins

---

## 🔑 CONCEPTOS CLAVE

### Multi-Tenant
- Cada gimnasio tiene sus datos aislados
- Middleware `gym_context` inyecta el contexto del gimnasio
- Repositories filtran automáticamente por `gimnasio_id`

### Dependency Injection
- FastAPI proporciona inyección de dependencias nativa
- Services reciben repositories inyectados
- Facilita testing y desacoplamiento

### Repository Pattern
- Abstrae el acceso a datos
- Facilita cambio de BD o caché
- Centraliza queries complejas

---

## 📦 PRÓXIMOS PASOS

1. ✅ Estructura creada
2. ⏳ Configuración inicial (config, database, security)
3. ⏳ Modelos SQLAlchemy
4. ⏳ Schemas Pydantic
5. ⏳ Repositories
6. ⏳ Services
7. ⏳ API Endpoints
8. ⏳ Middleware
9. ⏳ Tests
10. ⏳ Documentación

---

## 🚀 VENTAJAS DE ESTA ARQUITECTURA

✅ **Mantenibilidad**: Código organizado y fácil de mantener
✅ **Escalabilidad**: Fácil agregar nuevas funcionalidades
✅ **Testeable**: Testing unitario, integración y e2e
✅ **Reutilizable**: Código desacoplado y modular
✅ **Documentado**: Estructura autodocumentada
✅ **Multi-tenant**: Soporte nativo para múltiples gimnasios
✅ **Seguro**: Capas de seguridad bien definidas
✅ **Profesional**: Estándar de la industria