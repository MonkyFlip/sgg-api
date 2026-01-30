"""Enum de Estado de Membresía"""
from enum import Enum

class EstadoMembresiaEnum(str, Enum):
    """Estados de membresía"""
    ACTIVA = "ACTIVA"
    VENCIDA = "VENCIDA"
    CANCELADA = "CANCELADA"
    SUSPENDIDA = "SUSPENDIDA"
    
    def __str__(self):
        return self.value
    
    def permite_acceso(self) -> bool:
        """Verifica si el estado permite acceso al gimnasio"""
        return self == EstadoMembresiaEnum.ACTIVA
    
    def puede_renovar(self) -> bool:
        """Verifica si se puede renovar"""
        return self in [EstadoMembresiaEnum.VENCIDA, EstadoMembresiaEnum.ACTIVA]
    
    def es_valida(self) -> bool:
        """Verifica si es un estado válido"""
        return self in [EstadoMembresiaEnum.ACTIVA, EstadoMembresiaEnum.SUSPENDIDA]