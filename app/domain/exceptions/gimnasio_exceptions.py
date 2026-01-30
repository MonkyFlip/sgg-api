"""Excepciones de Gimnasio"""
from app.domain.exceptions.base import DomainException

class GimnasioNotFoundException(DomainException):
    """Excepción cuando no se encuentra un gimnasio"""
    
    def __init__(self, gimnasio_id: int = None, codigo: str = None):
        identifier = f"ID: {gimnasio_id}" if gimnasio_id else f"Código: {codigo}"
        super().__init__(
            message=f"Gimnasio no encontrado ({identifier})",
            code="GIMNASIO_NOT_FOUND",
            details={"gimnasio_id": gimnasio_id, "codigo": codigo}
        )

class GimnasioInactivoException(DomainException):
    """Excepción cuando un gimnasio está inactivo"""
    
    def __init__(self, gimnasio_id: int):
        super().__init__(
            message=f"El gimnasio con ID {gimnasio_id} está inactivo",
            code="GIMNASIO_INACTIVO",
            details={"gimnasio_id": gimnasio_id}
        )

class CodigoGimnasioDuplicadoException(DomainException):
    """Excepción cuando el código de gimnasio ya existe"""
    
    def __init__(self, codigo: str):
        super().__init__(
            message=f"El código de gimnasio '{codigo}' ya está en uso",
            code="CODIGO_GIMNASIO_DUPLICADO",
            details={"codigo": codigo}
        )