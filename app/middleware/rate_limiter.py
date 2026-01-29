"""
Middleware de Rate Limiting
Limita el número de requests por usuario/IP
"""

import time
from typing import Callable, Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar el rate de requests.
    
    Implementa:
    - Rate limiting por IP
    - Rate limiting por usuario
    - Ventanas de tiempo configurables
    - Endpoints excluidos
    """
    
    def __init__(self, app, calls_per_minute: int = None, calls_per_hour: int = None):
        """
        Inicializa el rate limiter.
        
        Args:
            app: Aplicación FastAPI
            calls_per_minute: Límite de calls por minuto (default de settings)
            calls_per_hour: Límite de calls por hora (default de settings)
        """
        super().__init__(app)
        
        self.calls_per_minute = calls_per_minute or settings.RATE_LIMIT_PER_MINUTE
        self.calls_per_hour = calls_per_hour or settings.RATE_LIMIT_PER_HOUR
        
        # Almacenamiento en memoria de contadores
        # En producción, usar Redis para compartir entre instancias
        self.minute_counters: Dict[str, list] = defaultdict(list)
        self.hour_counters: Dict[str, list] = defaultdict(list)
        
        # Rutas excluidas de rate limiting
        self.excluded_paths = [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/ping",
        ]
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa el request y aplica rate limiting.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
            
        Raises:
            HTTPException: Si se excede el rate limit
        """
        
        # Verificar si la ruta está excluida
        if self._is_excluded_path(request.url.path):
            return await call_next(request)
        
        # Obtener identificador único del cliente
        client_id = self._get_client_id(request)
        
        # Limpiar contadores antiguos
        self._cleanup_old_requests(client_id)
        
        # Verificar límites
        current_time = time.time()
        
        # Verificar límite por minuto
        if not self._check_limit(
            self.minute_counters[client_id],
            self.calls_per_minute,
            60,  # 60 segundos
            current_time
        ):
            logger.warning(
                f"Rate limit exceeded (per minute): {client_id}",
                client_id=client_id,
                path=request.url.path,
                limit=self.calls_per_minute
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Límite de {self.calls_per_minute} requests por minuto excedido",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.calls_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(current_time + 60))
                }
            )
        
        # Verificar límite por hora
        if not self._check_limit(
            self.hour_counters[client_id],
            self.calls_per_hour,
            3600,  # 3600 segundos (1 hora)
            current_time
        ):
            logger.warning(
                f"Rate limit exceeded (per hour): {client_id}",
                client_id=client_id,
                path=request.url.path,
                limit=self.calls_per_hour
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Límite de {self.calls_per_hour} requests por hora excedido",
                headers={
                    "Retry-After": "3600",
                    "X-RateLimit-Limit": str(self.calls_per_hour),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(current_time + 3600))
                }
            )
        
        # Registrar este request
        self.minute_counters[client_id].append(current_time)
        self.hour_counters[client_id].append(current_time)
        
        # Procesar request
        response = await call_next(request)
        
        # Agregar headers de rate limit a la respuesta
        remaining_minute = self.calls_per_minute - len(self.minute_counters[client_id])
        remaining_hour = self.calls_per_hour - len(self.hour_counters[client_id])
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(max(0, remaining_minute))
        response.headers["X-RateLimit-Limit-Hour"] = str(self.calls_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(max(0, remaining_hour))
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """
        Obtiene un identificador único del cliente.
        
        Prioridad:
        1. user_id (si está autenticado)
        2. IP address
        
        Args:
            request: Request de FastAPI
            
        Returns:
            str: Identificador único del cliente
        """
        # Si está autenticado, usar user_id
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user_{user_id}"
        
        # Si no, usar IP
        client_host = request.client.host if request.client else "unknown"
        
        # Considerar X-Forwarded-For si está detrás de un proxy
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_host = forwarded.split(",")[0].strip()
        
        return f"ip_{client_host}"
    
    def _is_excluded_path(self, path: str) -> bool:
        """
        Verifica si una ruta está excluida de rate limiting.
        
        Args:
            path: Path de la URL
            
        Returns:
            bool: True si está excluida
        """
        for excluded_path in self.excluded_paths:
            if path.startswith(excluded_path):
                return True
        return False
    
    def _check_limit(
        self,
        requests: list,
        limit: int,
        window: int,
        current_time: float
    ) -> bool:
        """
        Verifica si se está dentro del límite permitido.
        
        Args:
            requests: Lista de timestamps de requests
            limit: Límite de requests permitidos
            window: Ventana de tiempo en segundos
            current_time: Tiempo actual
            
        Returns:
            bool: True si está dentro del límite
        """
        # Filtrar requests dentro de la ventana de tiempo
        cutoff_time = current_time - window
        recent_requests = [t for t in requests if t > cutoff_time]
        
        # Actualizar la lista
        requests.clear()
        requests.extend(recent_requests)
        
        # Verificar si está dentro del límite
        return len(recent_requests) < limit
    
    def _cleanup_old_requests(self, client_id: str) -> None:
        """
        Limpia requests antiguos de los contadores.
        
        Args:
            client_id: Identificador del cliente
        """
        current_time = time.time()
        
        # Limpiar contador de minutos (requests más viejos de 1 minuto)
        if client_id in self.minute_counters:
            self.minute_counters[client_id] = [
                t for t in self.minute_counters[client_id]
                if current_time - t < 60
            ]
        
        # Limpiar contador de horas (requests más viejos de 1 hora)
        if client_id in self.hour_counters:
            self.hour_counters[client_id] = [
                t for t in self.hour_counters[client_id]
                if current_time - t < 3600
            ]


# ============================================
# RATE LIMITER CON REDIS (PRODUCCIÓN)
# ============================================

class RedisRateLimiter:
    """
    Rate limiter usando Redis para compartir estado entre instancias.
    
    Uso en producción cuando hay múltiples instancias de la API.
    
    Requiere:
    - redis-py instalado
    - Redis server configurado
    """
    
    def __init__(self, redis_client, prefix: str = "rate_limit"):
        """
        Inicializa el rate limiter con Redis.
        
        Args:
            redis_client: Cliente de Redis
            prefix: Prefijo para las keys en Redis
        """
        self.redis = redis_client
        self.prefix = prefix
    
    async def check_rate_limit(
        self,
        client_id: str,
        limit: int,
        window: int
    ) -> Tuple[bool, int]:
        """
        Verifica el rate limit usando Redis.
        
        Args:
            client_id: Identificador del cliente
            limit: Límite de requests
            window: Ventana de tiempo en segundos
            
        Returns:
            Tuple[bool, int]: (permitido, requests_restantes)
        """
        key = f"{self.prefix}:{client_id}:{window}"
        
        # Obtener contador actual
        current = await self.redis.get(key)
        current = int(current) if current else 0
        
        # Verificar límite
        if current >= limit:
            return False, 0
        
        # Incrementar contador
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        await pipe.execute()
        
        remaining = limit - (current + 1)
        return True, remaining


# ============================================
# DECORADOR PARA RATE LIMITING ESPECÍFICO
# ============================================

def rate_limit(calls: int, period: int):
    """
    Decorador para aplicar rate limiting a endpoints específicos.
    
    Uso:
    ```python
    @router.post("/expensive-operation")
    @rate_limit(calls=5, period=60)  # 5 calls por minuto
    async def expensive_operation():
        pass
    ```
    
    Args:
        calls: Número de llamadas permitidas
        period: Período en segundos
        
    Returns:
        Callable: Decorator function
    """
    def decorator(func):
        from functools import wraps
        
        # Almacenamiento en memoria (usar Redis en producción)
        counters: Dict[str, list] = defaultdict(list)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener request
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # Si no hay request, ejecutar sin rate limit
                return await func(*args, **kwargs)
            
            # Obtener client ID
            user_id = getattr(request.state, "user_id", None)
            client_id = f"user_{user_id}" if user_id else f"ip_{request.client.host}"
            
            # Verificar límite
            current_time = time.time()
            cutoff_time = current_time - period
            
            # Limpiar requests antiguos
            counters[client_id] = [
                t for t in counters[client_id]
                if t > cutoff_time
            ]
            
            # Verificar si excede el límite
            if len(counters[client_id]) >= calls:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Límite de {calls} requests por {period} segundos excedido"
                )
            
            # Registrar request
            counters[client_id].append(current_time)
            
            # Ejecutar función
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator