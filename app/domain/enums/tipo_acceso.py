"""Enum de Tipo de Acceso"""
from enum import Enum

class TipoAccesoEnum(str, Enum):
    """Tipos de acceso al gimnasio"""
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    CLASE = "CLASE"
    ENTRENAMIENTO_PERSONAL = "ENTRENAMIENTO_PERSONAL"
    EVENTO_ESPECIAL = "EVENTO_ESPECIAL"
    
    def __str__(self):
        return self.value
    
    def es_entrada(self) -> bool:
        """Verifica si es tipo entrada"""
        return self == TipoAccesoEnum.ENTRADA
    
    def requiere_reserva(self) -> bool:
        """Verifica si requiere reserva previa"""
        return self in [TipoAccesoEnum.CLASE, TipoAccesoEnum.ENTRENAMIENTO_PERSONAL]