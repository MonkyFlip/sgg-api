"""Gimnasio Entity"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class GimnasioEntity:
    """Entidad de dominio para Gimnasio"""
    id: Optional[int]
    nombre: str
    codigo_unico: str
    email: str
    activo: bool = True
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    
    def esta_activo(self) -> bool:
        """Verifica si el gimnasio está activo"""
        return self.activo
    
    def validar_codigo_unico(self) -> bool:
        """Valida que el código único tenga el formato correcto"""
        return len(self.codigo_unico) >= 3 and self.codigo_unico.isalnum()