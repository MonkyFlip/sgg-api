"""Enum de Estado de Factura"""
from enum import Enum

class EstadoFacturaEnum(str, Enum):
    """Estados de factura"""
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    CANCELADA = "CANCELADA"
    VENCIDA = "VENCIDA"
    
    def __str__(self):
        return self.value
    
    def permite_pago(self) -> bool:
        """Verifica si el estado permite realizar pagos"""
        return self in [EstadoFacturaEnum.PENDIENTE, EstadoFacturaEnum.VENCIDA]
    
    def es_final(self) -> bool:
        """Verifica si es un estado final (no cambia)"""
        return self in [EstadoFacturaEnum.PAGADA, EstadoFacturaEnum.CANCELADA]