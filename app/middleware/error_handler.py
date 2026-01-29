"""
Middleware de Manejo de Errores
Captura y procesa excepciones globalmente
"""

import traceback
from typing import Callable, Union
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.exc import IntegrityError, OperationalError

from app.core.logging import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware para capturar y manejar errores globalmente.
    
    Maneja:
    - Errores de validación
    - Errores de base de datos
    - Errores HTTP
    - Errores no controlados
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Union[Response, JSONResponse]:
        """
        Procesa el request y captura excepciones.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta normal o JSONResponse con error
        """
        
        try:
            response = await call_next(request)
            return response
            
        except Exception as e:
            return await self.handle_exception(request, e)
    
    async def handle_exception(
        self, request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Maneja una excepción y retorna una respuesta apropiada.
        
        Args:
            request: Request de FastAPI
            exc: Excepción capturada
            
        Returns:
            JSONResponse: Respuesta de error formateada
        """
        
        # Información del request para logging
        path = request.url.path
        method = request.method
        user_id = getattr(request.state, "user_id", None)
        
        # ==================================================
        # ERRORES DE BASE DE DATOS
        # ==================================================
        
        if isinstance(exc, IntegrityError):
            logger.error(
                f"Database integrity error en {method} {path}: {str(exc)}",
                user_id=user_id,
                exc_info=True
            )
            
            # Detectar tipo de error de integridad
            error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
            
            if "Duplicate entry" in error_msg or "UNIQUE constraint" in error_msg:
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={
                        "detail": "El registro ya existe",
                        "error_type": "duplicate_entry",
                        "path": path
                    }
                )
            
            elif "foreign key constraint" in error_msg.lower():
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "detail": "Referencia inválida a otro registro",
                        "error_type": "foreign_key_violation",
                        "path": path
                    }
                )
            
            else:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "detail": "Error de integridad de datos",
                        "error_type": "integrity_error",
                        "path": path
                    }
                )
        
        if isinstance(exc, OperationalError):
            logger.critical(
                f"Database operational error en {method} {path}: {str(exc)}",
                user_id=user_id,
                exc_info=True
            )
            
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "detail": "Error de conexión con la base de datos",
                    "error_type": "database_error",
                    "path": path
                }
            )
        
        # ==================================================
        # ERRORES HTTP (FastAPI HTTPException)
        # ==================================================
        
        from fastapi import HTTPException
        
        if isinstance(exc, HTTPException):
            logger.warning(
                f"HTTP {exc.status_code} en {method} {path}: {exc.detail}",
                user_id=user_id,
                status_code=exc.status_code
            )
            
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "detail": exc.detail,
                    "path": path
                },
                headers=exc.headers
            )
        
        # ==================================================
        # ERRORES DE VALIDACIÓN (Pydantic)
        # ==================================================
        
        from pydantic import ValidationError
        
        if isinstance(exc, ValidationError):
            logger.warning(
                f"Validation error en {method} {path}",
                user_id=user_id,
                errors=exc.errors()
            )
            
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={
                    "detail": "Error de validación",
                    "errors": exc.errors(),
                    "path": path
                }
            )
        
        # ==================================================
        # ERRORES PERSONALIZADOS DE DOMINIO
        # ==================================================
        
        # Aquí puedes agregar tus propias excepciones personalizadas
        # from app.domain.exceptions import UsuarioNotFoundException
        # if isinstance(exc, UsuarioNotFoundException):
        #     return JSONResponse(...)
        
        # ==================================================
        # ERRORES NO CONTROLADOS
        # ==================================================
        
        # Log detallado del error
        logger.critical(
            f"Unhandled exception en {method} {path}: {str(exc)}",
            user_id=user_id,
            exc_info=True,
            stack_trace=traceback.format_exc()
        )
        
        # En desarrollo, mostrar detalles del error
        if settings.DEBUG:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Error interno del servidor",
                    "error": str(exc),
                    "type": type(exc).__name__,
                    "path": path,
                    "traceback": traceback.format_exc().split("\n") if settings.DEBUG else None
                }
            )
        
        # En producción, mensaje genérico
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor. Por favor contacta al soporte.",
                "error_type": "internal_error",
                "path": path
            }
        )


# ============================================
# EXCEPTION HANDLERS ESPECÍFICOS
# ============================================

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler específico para errores de validación de Pydantic.
    
    Args:
        request: Request de FastAPI
        exc: Excepción de validación
        
    Returns:
        JSONResponse: Respuesta formateada
    """
    from pydantic import ValidationError
    
    if not isinstance(exc, ValidationError):
        raise exc
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación de datos",
            "errors": [
                {
                    "field": ".".join(str(loc) for loc in error["loc"]),
                    "message": error["msg"],
                    "type": error["type"]
                }
                for error in exc.errors()
            ]
        }
    )


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler específico para HTTPException de FastAPI.
    
    Args:
        request: Request de FastAPI
        exc: HTTPException
        
    Returns:
        JSONResponse: Respuesta formateada
    """
    from fastapi import HTTPException
    
    if not isinstance(exc, HTTPException):
        raise exc
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        },
        headers=exc.headers
    )


async def database_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler específico para errores de base de datos.
    
    Args:
        request: Request de FastAPI
        exc: Excepción de SQLAlchemy
        
    Returns:
        JSONResponse: Respuesta formateada
    """
    logger.error(
        f"Database error: {str(exc)}",
        path=request.url.path,
        exc_info=True
    )
    
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": "Conflicto con datos existentes",
                "error_type": "integrity_error"
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Error de base de datos",
            "error_type": "database_error"
        }
    )


# ============================================
# CUSTOM ERROR RESPONSES
# ============================================

def error_response(
    status_code: int,
    message: str,
    error_type: str = None,
    details: dict = None
) -> JSONResponse:
    """
    Crea una respuesta de error estandarizada.
    
    Args:
        status_code: Código HTTP de status
        message: Mensaje de error
        error_type: Tipo de error (opcional)
        details: Detalles adicionales (opcional)
        
    Returns:
        JSONResponse: Respuesta de error formateada
    """
    content = {
        "detail": message,
        "status_code": status_code
    }
    
    if error_type:
        content["error_type"] = error_type
    
    if details:
        content["details"] = details
    
    return JSONResponse(
        status_code=status_code,
        content=content
    )


def bad_request(message: str = "Solicitud incorrecta") -> JSONResponse:
    """Respuesta 400 Bad Request"""
    return error_response(status.HTTP_400_BAD_REQUEST, message, "bad_request")


def unauthorized(message: str = "No autorizado") -> JSONResponse:
    """Respuesta 401 Unauthorized"""
    return error_response(status.HTTP_401_UNAUTHORIZED, message, "unauthorized")


def forbidden(message: str = "Acceso prohibido") -> JSONResponse:
    """Respuesta 403 Forbidden"""
    return error_response(status.HTTP_403_FORBIDDEN, message, "forbidden")


def not_found(message: str = "Recurso no encontrado") -> JSONResponse:
    """Respuesta 404 Not Found"""
    return error_response(status.HTTP_404_NOT_FOUND, message, "not_found")


def conflict(message: str = "Conflicto con el estado actual") -> JSONResponse:
    """Respuesta 409 Conflict"""
    return error_response(status.HTTP_409_CONFLICT, message, "conflict")


def internal_error(message: str = "Error interno del servidor") -> JSONResponse:
    """Respuesta 500 Internal Server Error"""
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, "internal_error")