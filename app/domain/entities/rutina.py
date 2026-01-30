"""Rutina Entity"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class RutinaEntity:
    """Entidad de dominio para Rutina"""
    id: Optional[int]
    nombre: str
    gimnasio_id: int
    creador_id: int
    nivel: str
    tipo: str
    activo: bool = True
    cliente_id: Optional[int] = None
    duracion_semanas: Optional[int] = None
    
    def es_personalizada(self) -> bool:
        """Verifica si es una rutina personalizada"""
        return self.cliente_id is not None
    
    def es_general(self) -> bool:
        """Verifica si es una rutina general"""
        return self.cliente_id is None
    
    def validar_nivel(self) -> bool:
        """Valida que el nivel sea correcto"""
        niveles_validos = ["PRINCIPIANTE", "INTERMEDIO", "AVANZADO", "EXPERTO"]
        return self.nivel.upper() in niveles_validos