"""
Aplicación principal de FastAPI - Sistema de Gestión de Gimnasios
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.domain.exceptions.base import DomainException

# Importar todos los modelos para que SQLAlchemy los registre
from app.models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contexto de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.
    """
    # Startup
    print("🚀 Iniciando aplicación...")
    print(f"📊 Base de datos: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    
    # Crear tablas si no existen (en producción usar Alembic)
    # Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    print("👋 Cerrando aplicación...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API REST para Sistema de Gestión de Gimnasios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers de la API
app.include_router(api_router, prefix="/api/v1")

# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Maneja excepciones de dominio"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.to_dict()
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Error de validación en los datos enviados",
            "details": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Maneja excepciones no capturadas"""
    print(f"❌ Error no manejado: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Error interno del servidor"
        }
    )

# ==================== ENDPOINTS BASE ====================

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz"""
    return {
        "message": "SGG API - Sistema de Gestión de Gimnasios",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Verificación de salud de la API"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )