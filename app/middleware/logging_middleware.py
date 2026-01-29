"""
Middleware de Logging
Registra todas las requests HTTP con detalles importantes
"""

import time
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para loggear todas las requests HTTP.
    
    Registra:
    - Método HTTP
    - Path
    - Query params
    - Status code
    - Tiempo de respuesta
    - Usuario (si está autenticado)
    - IP del cliente
    - User-Agent
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa el request y registra información relevante.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
        """
        
        # Tiempo de inicio
        start_time = time.time()
        
        # Información del request
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else None
        client_host = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        
        # Información del usuario autenticado (si existe)
        user_id = getattr(request.state, "user_id", None)
        gimnasio_id = getattr(request.state, "gimnasio_id", None)
        
        # Procesar request
        try:
            response = await call_next(request)
            status_code = response.status_code
            
        except Exception as e:
            # Si hay error, registrar y re-lanzar
            duration = time.time() - start_time
            
            logger.error(
                f"ERROR en {method} {path} - {str(e)}",
                method=method,
                path=path,
                query_params=query_params,
                user_id=user_id,
                gimnasio_id=gimnasio_id,
                client_host=client_host,
                user_agent=user_agent,
                duration=duration,
                exc_info=True
            )
            raise
        
        # Calcular duración
        duration = time.time() - start_time
        
        # Determinar nivel de log según status code
        if status_code >= 500:
            log_level = logger.error
        elif status_code >= 400:
            log_level = logger.warning
        else:
            log_level = logger.info
        
        # Log del request completado
        log_level(
            f"{method} {path} - {status_code} - {duration:.3f}s",
            method=method,
            path=path,
            query_params=query_params,
            status_code=status_code,
            duration=duration,
            user_id=user_id,
            gimnasio_id=gimnasio_id,
            client_host=client_host,
            user_agent=user_agent
        )
        
        # Agregar headers personalizados a la respuesta
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        return response


# ============================================
# LOGGING DETALLADO PARA DEBUG
# ============================================

class DetailedLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging muy detallado (solo para desarrollo/debug).
    
    ⚠️ NO USAR EN PRODUCCIÓN - puede exponer información sensible
    
    Registra:
    - Headers completos
    - Body del request (si es pequeño)
    - Body del response (si es pequeño)
    """
    
    MAX_BODY_SIZE = 1000  # bytes
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa el request con logging detallado.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
        """
        
        # Log de headers
        logger.debug(
            f"Request headers: {dict(request.headers)}",
            path=request.url.path
        )
        
        # Log de body (si no es muy grande)
        try:
            body = await request.body()
            if len(body) < self.MAX_BODY_SIZE and body:
                logger.debug(
                    f"Request body: {body.decode('utf-8')}",
                    path=request.url.path
                )
        except Exception:
            pass
        
        # Procesar request
        response = await call_next(request)
        
        # Log de response headers
        logger.debug(
            f"Response headers: {dict(response.headers)}",
            path=request.url.path,
            status_code=response.status_code
        )
        
        return response


# ============================================
# LOGGING DE QUERIES SQL (OPCIONAL)
# ============================================

class SQLLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para loggear queries SQL ejecutadas durante un request.
    
    Útil para debugging y optimización de queries.
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa el request y registra queries SQL.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
        """
        
        # Contador de queries para este request
        request.state.sql_query_count = 0
        request.state.sql_query_time = 0.0
        
        # Procesar request
        response = await call_next(request)
        
        # Log de estadísticas SQL
        query_count = getattr(request.state, "sql_query_count", 0)
        query_time = getattr(request.state, "sql_query_time", 0.0)
        
        if query_count > 0:
            logger.info(
                f"SQL Stats: {query_count} queries en {query_time:.3f}s",
                path=request.url.path,
                query_count=query_count,
                query_time=query_time,
                avg_query_time=query_time / query_count if query_count > 0 else 0
            )
            
            # Alerta si hay demasiadas queries (N+1 problem)
            if query_count > 20:
                logger.warning(
                    f"⚠️ Posible N+1 problem: {query_count} queries en {request.url.path}",
                    path=request.url.path,
                    query_count=query_count
                )
        
        return response


# ============================================
# HELPERS PARA LOGGING PERSONALIZADO
# ============================================

def log_request_body(request: Request) -> None:
    """
    Helper para loggear el body de un request manualmente.
    
    Uso en endpoints:
    ```python
    @router.post("/usuarios")
    async def create_user(request: Request, data: UsuarioCreate):
        log_request_body(request)
        # ...
    ```
    
    Args:
        request: Request de FastAPI
    """
    try:
        # El body ya fue leído, usar el state si se guardó
        body = getattr(request.state, "body", None)
        if body:
            logger.debug(
                f"Request body logged manually: {body}",
                path=request.url.path
            )
    except Exception as e:
        logger.warning(f"No se pudo loggear body: {str(e)}")


def log_business_action(
    action: str,
    entity: str,
    entity_id: int = None,
    details: dict = None
) -> None:
    """
    Helper para loggear acciones de negocio importantes.
    
    Uso:
    ```python
    log_business_action(
        action="CREATE",
        entity="Usuario",
        entity_id=user.id,
        details={"email": user.email, "role": user.role}
    )
    ```
    
    Args:
        action: Acción realizada (CREATE, UPDATE, DELETE, etc.)
        entity: Entidad afectada
        entity_id: ID de la entidad (opcional)
        details: Detalles adicionales (opcional)
    """
    logger.info(
        f"Business Action: {action} - {entity}" + (f":{entity_id}" if entity_id else ""),
        action=action,
        entity=entity,
        entity_id=entity_id,
        details=details or {}
    )