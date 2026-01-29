"""
Modelo Rol
Representa los roles del sistema (super_admin, admin, entrenador, cliente)
"""

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base


class Rol(Base):
    """
    Modelo de Rol.
    
    Define los roles disponibles en el sistema:
    - super_admin: Administrador del gimnasio con acceso total
    - admin: Administrador con permisos limitados
    - entrenador: Entrenador personal
    - cliente: Cliente del gimnasio
    """
    
    __tablename__ = "roles"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Nombre del rol (super_admin, admin, entrenador, cliente)"
    )
    descripcion = Column(String(255), nullable=True, comment="Descripción del rol")
    permisos = Column(JSON, nullable=True, comment="Permisos del rol en formato JSON")
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
    
    def __repr__(self):
        return f"<Rol(id={self.id}, nombre='{self.nombre}')>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "permisos": self.permisos,
        }
    
    def tiene_permiso(self, permiso: str) -> bool:
        """
        Verifica si el rol tiene un permiso específico.
        
        Args:
            permiso: Nombre del permiso a verificar
            
        Returns:
            bool: True si tiene el permiso
        """
        if not self.permisos:
            return False
        
        # Si tiene permiso "all", tiene todos los permisos
        if self.permisos.get("all"):
            return True
        
        # Buscar el permiso específico
        return permiso in self.permisos