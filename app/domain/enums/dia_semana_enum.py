"""Enum de Día de la Semana"""
from enum import Enum

class DiaSemanaEnum(str, Enum):
    """Días de la semana"""
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIERCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SABADO"
    DOMINGO = "DOMINGO"
    
    def __str__(self):
        return self.value
    
    def es_fin_semana(self) -> bool:
        """Verifica si es fin de semana"""
        return self in [DiaSemanaEnum.SABADO, DiaSemanaEnum.DOMINGO]
    
    def es_dia_laboral(self) -> bool:
        """Verifica si es día laboral"""
        return not self.es_fin_semana()
    
    @classmethod
    def from_numero(cls, numero: int):
        """Obtiene día desde número (0=Lunes, 6=Domingo)"""
        dias = [cls.LUNES, cls.MARTES, cls.MIERCOLES, cls.JUEVES, 
                cls.VIERNES, cls.SABADO, cls.DOMINGO]
        return dias[numero % 7]