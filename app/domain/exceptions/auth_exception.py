"""Excepciones de Autenticación"""
from app.domain.exceptions.base import DomainException

class AuthenticationException(DomainException):
    """Excepción base de autenticación"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message=message,
            code="AUTHENTICATION_ERROR",
            details=details
        )

class InvalidCredentialsException(AuthenticationException):
    """Excepción cuando las credenciales son inválidas"""
    
    def __init__(self):
        super().__init__(
            message="Email o contraseña incorrectos",
            details={}
        )

class TokenExpiredException(AuthenticationException):
    """Excepción cuando el token ha expirado"""
    
    def __init__(self):
        super().__init__(
            message="El token ha expirado",
            details={}
        )

class UnauthorizedException(AuthenticationException):
    """Excepción cuando no está autorizado"""
    
    def __init__(self, accion: str = None):
        mensaje = "No autorizado"
        if accion:
            mensaje += f" para {accion}"
        
        super().__init__(
            message=mensaje,
            details={"accion": accion}
        )

class PermisosInsuficientesException(AuthenticationException):
    """Excepción cuando no tiene permisos suficientes"""
    
    def __init__(self, recurso: str):
        super().__init__(
            message=f"No tienes permisos para acceder a {recurso}",
            details={"recurso": recurso}
        )