"""Usuario Entity"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class UsuarioEntity:
    """Entidad de dominio para Usuario"""
    id: Optional[int]
    nombre: str
    apellido: str
    email: str
    gimnasio_id: int
    rol_nombre: str
    fecha_nacimiento: Optional[date] = None
    activo: bool = True
    
    @property
    def nombre_completo(self) -> str:
        """Retorna nombre completo"""
        return f"{self.nombre} {self.apellido}"
    
    @property
    def edad(self) -> Optional[int]:
        """Calcula edad del usuario"""
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad
    
    def es_mayor_edad(self) -> bool:
        """Verifica si es mayor de edad"""
        return self.edad >= 18 if self.edad else False
    
    def es_admin(self) -> bool:
        """Verifica si es administrador"""
        return self.rol_nombre.lower() in ['admin', 'administrador', 'super_admin']
    
    def es_entrenador(self) -> bool:
        """Verifica si es entrenador"""
        return self.rol_nombre.lower() == 'entrenador'
    
    def es_cliente(self) -> bool:
        """Verifica si es cliente"""
        return self.rol_nombre.lower() == 'cliente'
    
    def puede_acceder(self) -> bool:
        """Verifica si puede acceder al gimnasio"""
        return self.activo