"""Clase Entity"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class ClaseEntity:
    """Entidad de dominio para Clase"""
    id: Optional[int]
    nombre: str
    gimnasio_id: int
    entrenador_id: int
    capacidad_maxima: int
    duracion_minutos: int
    activo: bool = True
    descripcion: Optional[str] = None
    
    def tiene_cupo_disponible(self, reservas_actuales: int) -> bool:
        """Verifica si hay cupo disponible"""
        return reservas_actuales < self.capacidad_maxima
    
    def cupos_disponibles(self, reservas_actuales: int) -> int:
        """Calcula cupos disponibles"""
        return max(0, self.capacidad_maxima - reservas_actuales)