"""
Middleware de Contexto de Gimnasio
Establece el contexto del gimnasio actual para requests multi-tenant
"""

from typing import Callable, Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class GymContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware para establecer el contexto del gimnasio en cada request.
    
    Este middleware es crucial para la arquitectura multi-tenant:
    - Extrae el gimnasio_id del usuario autenticado
    - Lo hace disponible en request.state.gimnasio_id
    - Permite que repositories filtren automáticamente por gimnasio
    """
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Establece el contexto del gimnasio para el request actual.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
        """
        
        # Intentar obtener gimnasio_id del state (agregado por AuthenticationMiddleware)
        gimnasio_id = getattr(request.state, "gimnasio_id", None)
        
        # También podría venir en los headers (para casos especiales)
        if not gimnasio_id:
            gimnasio_id = request.headers.get("X-Gym-ID")
        
        # También podría venir en query params (para webhooks, etc.)
        if not gimnasio_id:
            gimnasio_id = request.query_params.get("gimnasio_id")
        
        # Establecer contexto del gimnasio
        if gimnasio_id:
            request.state.gym_context = {
                "gimnasio_id": int(gimnasio_id) if isinstance(gimnasio_id, str) else gimnasio_id,
                "is_active": True,  # Aquí podrías validar si el gimnasio está activo
            }
            
            logger.debug(
                f"Contexto de gimnasio establecido: {gimnasio_id}",
                gimnasio_id=gimnasio_id,
                path=request.url.path
            )
        else:
            request.state.gym_context = None
            logger.debug(
                f"Sin contexto de gimnasio para: {request.url.path}",
                path=request.url.path
            )
        
        # Continuar con el request
        response = await call_next(request)
        
        return response


# ============================================
# FUNCIONES HELPER PARA OBTENER CONTEXTO
# ============================================

def get_gym_context(request: Request) -> Optional[dict]:
    """
    Obtiene el contexto del gimnasio del request actual.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        dict: Contexto del gimnasio o None
    """
    return getattr(request.state, "gym_context", None)


def get_current_gym_id(request: Request) -> Optional[int]:
    """
    Obtiene el ID del gimnasio actual del contexto.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        int: ID del gimnasio o None
    """
    gym_context = get_gym_context(request)
    if gym_context:
        return gym_context.get("gimnasio_id")
    return None


def ensure_gym_context(request: Request) -> int:
    """
    Asegura que exista un contexto de gimnasio válido.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        int: ID del gimnasio
        
    Raises:
        ValueError: Si no hay contexto de gimnasio
    """
    gimnasio_id = get_current_gym_id(request)
    
    if not gimnasio_id:
        raise ValueError("No se pudo determinar el contexto del gimnasio")
    
    return gimnasio_id


# ============================================
# CONTEXT MANAGER PARA OPERACIONES DE BD
# ============================================

class GymScope:
    """
    Context manager para asegurar que las operaciones de BD
    estén dentro del scope del gimnasio correcto.
    
    Uso:
    ```python
    with GymScope(gimnasio_id=1):
        usuarios = usuario_repository.get_all()
        # Solo retorna usuarios del gimnasio 1
    ```
    """
    
    _current_gym_id: Optional[int] = None
    
    def __init__(self, gimnasio_id: int):
        self.gimnasio_id = gimnasio_id
        self.previous_gym_id = None
    
    def __enter__(self):
        """Establece el contexto del gimnasio"""
        self.previous_gym_id = GymScope._current_gym_id
        GymScope._current_gym_id = self.gimnasio_id
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restaura el contexto anterior"""
        GymScope._current_gym_id = self.previous_gym_id
    
    @classmethod
    def get_current_gym_id(cls) -> Optional[int]:
        """Obtiene el ID del gimnasio en el scope actual"""
        return cls._current_gym_id
    
    @classmethod
    def is_in_scope(cls) -> bool:
        """Verifica si estamos dentro de un GymScope"""
        return cls._current_gym_id is not None


# ============================================
# DECORADOR PARA FUNCIONES CON SCOPE
# ============================================

def with_gym_scope(func):
    """
    Decorador para asegurar que una función se ejecute
    dentro del scope del gimnasio del usuario actual.
    
    Uso:
    ```python
    @with_gym_scope
    async def get_usuarios(request: Request):
        # gimnasio_id está disponible automáticamente
        pass
    ```
    """
    from functools import wraps
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Buscar request en los argumentos
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        
        # Si no está en args, buscar en kwargs
        if not request and "request" in kwargs:
            request = kwargs["request"]
        
        if not request:
            # Si no hay request, ejecutar sin scope
            return await func(*args, **kwargs)
        
        # Obtener gimnasio_id del request
        gimnasio_id = get_current_gym_id(request)
        
        if not gimnasio_id:
            # Si no hay gimnasio_id, ejecutar sin scope
            return await func(*args, **kwargs)
        
        # Ejecutar dentro del scope del gimnasio
        with GymScope(gimnasio_id=gimnasio_id):
            return await func(*args, **kwargs)
    
    return wrapper


# ============================================
# VALIDADORES DE CONTEXTO
# ============================================

def validate_gym_access(request: Request, gimnasio_id: int) -> bool:
    """
    Valida que el usuario tenga acceso al gimnasio especificado.
    
    Args:
        request: Request de FastAPI
        gimnasio_id: ID del gimnasio a validar
        
    Returns:
        bool: True si tiene acceso
    """
    current_gym_id = get_current_gym_id(request)
    
    # Si no hay contexto, no tiene acceso
    if not current_gym_id:
        return False
    
    # Super admins pueden acceder a cualquier gimnasio (opcional)
    user_role = getattr(request.state, "role", None)
    if user_role == "super_admin":
        return True
    
    # Validar que el gimnasio coincida
    return current_gym_id == gimnasio_id


def require_gym_access(gimnasio_id: int):
    """
    Dependency para requerir acceso a un gimnasio específico.
    
    Uso:
    ```python
    @router.get("/gimnasios/{gimnasio_id}/usuarios")
    async def get_users(
        gimnasio_id: int,
        _: None = Depends(require_gym_access)
    ):
        pass
    ```
    
    Args:
        gimnasio_id: ID del gimnasio requerido
        
    Returns:
        Callable: Dependency function
    """
    async def check_access(request: Request) -> None:
        if not validate_gym_access(request, gimnasio_id):
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este gimnasio"
            )
    
    return check_access