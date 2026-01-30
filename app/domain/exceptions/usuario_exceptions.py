"""Excepciones de Usuario"""
from app.domain.exceptions.base import DomainException

class UsuarioNotFoundException(DomainException):
    """Excepción cuando no se encuentra un usuario"""
    
    def __init__(self, usuario_id: int = None, email: str = None):
        identifier = f"ID: {usuario_id}" if usuario_id else f"Email: {email}"
        super().__init__(
            message=f"Usuario no encontrado ({identifier})",
            code="USUARIO_NOT_FOUND",
            details={"usuario_id": usuario_id, "email": email}
        )

class UsuarioInactivoException(DomainException):
    """Excepción cuando un usuario está inactivo"""
    
    def __init__(self, usuario_id: int):
        super().__init__(
            message=f"El usuario con ID {usuario_id} está inactivo",
            code="USUARIO_INACTIVO",
            details={"usuario_id": usuario_id}
        )

class EmailDuplicadoException(DomainException):
    """Excepción cuando el email ya existe"""
    
    def __init__(self, email: str):
        super().__init__(
            message=f"El email '{email}' ya está registrado",
            code="EMAIL_DUPLICADO",
            details={"email": email}
        )

class UsuarioSinPermisosException(DomainException):
    """Excepción cuando el usuario no tiene permisos"""
    
    def __init__(self, accion: str):
        super().__init__(
            message=f"No tienes permisos para {accion}",
            code="SIN_PERMISOS",
            details={"accion": accion}
        )