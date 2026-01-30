"""Service de Autenticación"""
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.usuario import UsuarioRepository
from app.repositories.gimnasio import GimnasioRepository
from app.repositories.rol import RolRepository
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, verify_token, validate_password_strength
)
from app.schemas.auth import Login, Register, Token
from app.models.usuario import Usuario


class AuthService:
    """Servicio de autenticación y autorización"""
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.gimnasio_repo = GimnasioRepository(db)
        self.rol_repo = RolRepository(db)
    
    def login(self, login_data: Login) -> Token:
        """
        Autentica un usuario y genera tokens JWT.
        
        Args:
            login_data: Credenciales de login
            
        Returns:
            Token: Access token y refresh token
            
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        # Buscar usuario por email
        usuario = self.usuario_repo.get_by_email(login_data.email)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        # Verificar contraseña
        if not verify_password(login_data.password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        # Verificar que el usuario esté activo
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo. Contacta al administrador"
            )
        
        # Generar tokens
        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email,
                "role": usuario.rol.nombre,
                "gimnasio_id": usuario.gimnasio_id
            }
        )
        
        refresh_token = create_refresh_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email
            }
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    def register(self, register_data: Register) -> Usuario:
        """
        Registra un nuevo usuario (cliente).
        
        Args:
            register_data: Datos de registro
            
        Returns:
            Usuario: Usuario creado
            
        Raises:
            HTTPException: Si hay errores de validación
        """
        # Verificar que el email no esté en uso
        if self.usuario_repo.get_by_email(register_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Verificar que el gimnasio exista
        gimnasio = self.gimnasio_repo.get_by_codigo(register_data.gimnasio_codigo)
        if not gimnasio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código de gimnasio inválido"
            )
        
        # Validar fortaleza de contraseña
        if not validate_password_strength(register_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales"
            )
        
        # Obtener rol de cliente
        rol_cliente = self.rol_repo.get_by_nombre("cliente")
        if not rol_cliente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error de configuración: rol 'cliente' no encontrado"
            )
        
        # Crear usuario
        usuario_data = {
            "nombre": register_data.nombre,
            "apellido": register_data.apellido,
            "email": register_data.email,
            "password_hash": get_password_hash(register_data.password),
            "telefono": register_data.telefono,
            "gimnasio_id": gimnasio.id,
            "rol_id": rol_cliente.id,
            "activo": True
        }
        
        usuario = self.usuario_repo.create(usuario_data)
        return usuario
    
    def refresh_access_token(self, refresh_token: str) -> Token:
        """
        Genera un nuevo access token usando un refresh token.
        
        Args:
            refresh_token: Refresh token válido
            
        Returns:
            Token: Nuevo access token
            
        Raises:
            HTTPException: Si el refresh token es inválido
        """
        payload = verify_token(refresh_token, token_type="refresh")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado"
            )
        
        user_id = int(payload.get("sub"))
        usuario = self.usuario_repo.get_by_id(user_id)
        
        if not usuario or not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o inactivo"
            )
        
        # Generar nuevo access token
        access_token = create_access_token(
            data={
                "sub": str(usuario.id),
                "email": usuario.email,
                "role": usuario.rol.nombre,
                "gimnasio_id": usuario.gimnasio_id
            }
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer"
        )
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Cambia la contraseña de un usuario.
        
        Args:
            user_id: ID del usuario
            current_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            bool: True si se cambió exitosamente
            
        Raises:
            HTTPException: Si hay errores de validación
        """
        usuario = self.usuario_repo.get_by_id(user_id)
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not verify_password(current_password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña actual incorrecta"
            )
        
        # Validar nueva contraseña
        if not validate_password_strength(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña no cumple los requisitos de seguridad"
            )
        
        # Actualizar contraseña
        self.usuario_repo.update(user_id, {
            "password_hash": get_password_hash(new_password)
        })
        
        return True