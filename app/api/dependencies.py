"""Dependencias compartidas para los endpoints"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import verify_token
from app.repositories.usuario import UsuarioRepository
from app.models.usuario import Usuario

security = HTTPBearer()

def get_db() -> Generator:
    """
    Dependencia para obtener la sesión de base de datos.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependencia para obtener el usuario actual autenticado.
    
    Args:
        credentials: Credenciales del token Bearer
        db: Sesión de base de datos
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    
    # Verificar token
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Obtener usuario
    user_id = int(payload.get("sub"))
    usuario_repo = UsuarioRepository(db)
    usuario = usuario_repo.get_by_id(user_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return usuario

def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependencia para obtener usuario activo.
    """
    if not current_user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user

def require_admin(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependencia que requiere que el usuario sea administrador.
    """
    if not current_user.es_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return current_user

def require_entrenador(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """
    Dependencia que requiere que el usuario sea entrenador.
    """
    if not current_user.es_entrenador():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere ser entrenador"
        )
    return current_user

def get_gimnasio_id(
    current_user: Usuario = Depends(get_current_user)
) -> int:
    """
    Obtiene el ID del gimnasio del usuario actual.
    """
    return current_user.gimnasio_id