"""Excepciones de Membresía"""
from app.domain.exceptions.base import DomainException

class MembresiaNotFoundException(DomainException):
    """Excepción cuando no se encuentra una membresía"""
    
    def __init__(self, membresia_id: int = None, usuario_id: int = None):
        identifier = f"ID: {membresia_id}" if membresia_id else f"Usuario: {usuario_id}"
        super().__init__(
            message=f"Membresía no encontrada ({identifier})",
            code="MEMBRESIA_NOT_FOUND",
            details={"membresia_id": membresia_id, "usuario_id": usuario_id}
        )

class MembresiaVencidaException(DomainException):
    """Excepción cuando una membresía está vencida"""
    
    def __init__(self, membresia_id: int, fecha_vencimiento: str):
        super().__init__(
            message=f"La membresía venció el {fecha_vencimiento}",
            code="MEMBRESIA_VENCIDA",
            details={
                "membresia_id": membresia_id,
                "fecha_vencimiento": fecha_vencimiento
            }
        )

class MembresiaDuplicadaException(DomainException):
    """Excepción cuando ya existe una membresía activa"""
    
    def __init__(self, usuario_id: int):
        super().__init__(
            message=f"El usuario ya tiene una membresía activa",
            code="MEMBRESIA_DUPLICADA",
            details={"usuario_id": usuario_id}
        )

class SinMembresiaActivaException(DomainException):
    """Excepción cuando no hay membresía activa"""
    
    def __init__(self, usuario_id: int):
        super().__init__(
            message=f"El usuario no tiene una membresía activa",
            code="SIN_MEMBRESIA_ACTIVA",
            details={"usuario_id": usuario_id}
        )