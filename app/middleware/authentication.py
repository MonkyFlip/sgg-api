"""
Middleware de Autenticación
Maneja la verificación de tokens JWT en las requests
"""

from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.security import decode_token, verify_token
from app.core.logging import get_logger

logger = get_logger(__name__)

# Security scheme para Bearer token
security = HTTPBearer()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar tokens JWT en requests protegidos.
    
    Rutas excluidas de autenticación:
    - /docs, /redoc, /openapi.json (Documentación)
    - /api/v1/auth/* (Endpoints de autenticación)
    - /health, /ping (Health checks)
    """
    
    # Rutas que NO requieren autenticación
    EXCLUDED_PATHS = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/auth/forgot-password",
        "/api/v1/auth/reset-password",
        "/health",
        "/ping",
    ]
    
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Procesa cada request y valida el token JWT si es necesario.
        
        Args:
            request: Request de FastAPI
            call_next: Siguiente función en la cadena
            
        Returns:
            Response: Respuesta del endpoint
        """
        
        # Verificar si la ruta está excluida de autenticación
        if self._is_excluded_path(request.url.path):
            return await call_next(request)
        
        # Obtener token del header Authorization
        token = self._get_token_from_header(request)
        
        if not token:
            logger.warning(
                f"Request sin token: {request.method} {request.url.path}",
                ip=request.client.host if request.client else None
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación requerido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar y decodificar token
        payload = verify_token(token, token_type="access")
        
        if not payload:
            logger.warning(
                f"Token inválido o expirado: {request.method} {request.url.path}",
                ip=request.client.host if request.client else None
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Agregar información del usuario al state del request
        request.state.user_id = payload.get("sub")
        request.state.email = payload.get("email")
        request.state.role = payload.get("role")
        request.state.gimnasio_id = payload.get("gimnasio_id")
        
        logger.info(
            f"Request autenticado: {request.method} {request.url.path}",
            user_id=request.state.user_id,
            role=request.state.role,
            gimnasio_id=request.state.gimnasio_id
        )
        
        # Continuar con el siguiente middleware/endpoint
        response = await call_next(request)
        return response
    
    def _is_excluded_path(self, path: str) -> bool:
        """
        Verifica si una ruta está excluida de autenticación.
        
        Args:
            path: Path de la URL
            
        Returns:
            bool: True si está excluida
        """
        # Verificar coincidencias exactas
        if path in self.EXCLUDED_PATHS:
            return True
        
        # Verificar si empieza con alguna ruta excluida
        for excluded_path in self.EXCLUDED_PATHS:
            if path.startswith(excluded_path):
                return True
        
        return False
    
    def _get_token_from_header(self, request: Request) -> Optional[str]:
        """
        Extrae el token JWT del header Authorization.
        
        Args:
            request: Request de FastAPI
            
        Returns:
            str: Token JWT o None si no existe
        """
        authorization: str = request.headers.get("Authorization")
        
        if not authorization:
            return None
        
        # El formato debe ser: "Bearer <token>"
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return None
            return token
        except ValueError:
            return None


# ============================================
# DEPENDENCY PARA OBTENER USUARIO ACTUAL
# ============================================

async def get_current_user(request: Request) -> dict:
    """
    Dependency para obtener el usuario actual del request.
    
    Uso en endpoints:
    ```python
    @router.get("/me")
    async def get_me(current_user: dict = Depends(get_current_user)):
        return current_user
    ```
    
    Args:
        request: Request de FastAPI
        
    Returns:
        dict: Información del usuario actual
        
    Raises:
        HTTPException: Si no hay usuario autenticado
    """
    user_id = getattr(request.state, "user_id", None)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado"
        )
    
    return {
        "user_id": request.state.user_id,
        "email": request.state.email,
        "role": request.state.role,
        "gimnasio_id": request.state.gimnasio_id,
    }


async def get_current_active_user(request: Request) -> dict:
    """
    Dependency para obtener usuario activo (similar a get_current_user).
    Aquí podrías agregar validaciones adicionales como verificar
    si el usuario está activo en la base de datos.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        dict: Información del usuario activo
    """
    current_user = await get_current_user(request)
    
    # Aquí podrías agregar validación en BD:
    # user = await user_repository.get_by_id(current_user["user_id"])
    # if not user.activo:
    #     raise HTTPException(status_code=403, detail="Usuario inactivo")
    
    return current_user


# ============================================
# DEPENDENCIES DE AUTORIZACIÓN POR ROL
# ============================================

def require_role(allowed_roles: list[str]):
    """
    Decorator/Dependency para requerir roles específicos.
    
    Uso:
    ```python
    @router.delete("/usuarios/{id}")
    async def delete_user(
        id: int,
        current_user: dict = Depends(require_role(["super_admin", "admin"]))
    ):
        # Solo super_admin y admin pueden ejecutar este endpoint
        pass
    ```
    
    Args:
        allowed_roles: Lista de roles permitidos
        
    Returns:
        Callable: Función dependency
    """
    async def role_checker(request: Request) -> dict:
        current_user = await get_current_user(request)
        
        if current_user["role"] not in allowed_roles:
            logger.warning(
                f"Acceso denegado por rol: {request.method} {request.url.path}",
                user_id=current_user["user_id"],
                role=current_user["role"],
                required_roles=allowed_roles
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker


async def require_super_admin(request: Request) -> dict:
    """Dependency para requerir rol de Super Admin"""
    return await require_role(["super_admin"])(request)


async def require_admin(request: Request) -> dict:
    """Dependency para requerir rol de Admin o Super Admin"""
    return await require_role(["super_admin", "admin"])(request)


async def require_staff(request: Request) -> dict:
    """Dependency para requerir rol de Staff (Admin, Super Admin o Entrenador)"""
    return await require_role(["super_admin", "admin", "entrenador"])(request)


# ============================================
# DEPENDENCY PARA VERIFICAR GIMNASIO
# ============================================

def require_same_gym(gimnasio_id: int):
    """
    Dependency para verificar que el usuario pertenezca al mismo gimnasio.
    
    Uso:
    ```python
    @router.get("/gimnasios/{gimnasio_id}/usuarios")
    async def get_gym_users(
        gimnasio_id: int,
        current_user: dict = Depends(require_same_gym)
    ):
        # Usuario debe pertenecer al gimnasio solicitado
        pass
    ```
    
    Args:
        gimnasio_id: ID del gimnasio a validar
        
    Returns:
        Callable: Función dependency
    """
    async def gym_checker(request: Request) -> dict:
        current_user = await get_current_user(request)
        
        # Super admins pueden acceder a cualquier gimnasio (opcional)
        if current_user["role"] == "super_admin":
            return current_user
        
        if current_user["gimnasio_id"] != gimnasio_id:
            logger.warning(
                f"Acceso denegado: usuario de gimnasio {current_user['gimnasio_id']} "
                f"intentó acceder a gimnasio {gimnasio_id}",
                user_id=current_user["user_id"]
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes acceso a este gimnasio"
            )
        
        return current_user
    
    return gym_checker