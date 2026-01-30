"""Enum de Género"""
from enum import Enum

class GeneroEnum(str, Enum):
    """Géneros"""
    MASCULINO = "M"
    FEMENINO = "F"
    OTRO = "OTRO"
    NO_ESPECIFICADO = "NO_ESPECIFICADO"
    
    def __str__(self):
        return self.value
    
    @classmethod
    def from_string(cls, value: str):
        """Convierte string a enum"""
        mapping = {
            "M": cls.MASCULINO,
            "MASCULINO": cls.MASCULINO,
            "HOMBRE": cls.MASCULINO,
            "F": cls.FEMENINO,
            "FEMENINO": cls.FEMENINO,
            "MUJER": cls.FEMENINO,
            "OTRO": cls.OTRO,
            "NO_ESPECIFICADO": cls.NO_ESPECIFICADO,
        }
        return mapping.get(value.upper(), cls.NO_ESPECIFICADO)