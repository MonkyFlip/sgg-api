"""
Modelo Base y Mixins para SQLAlchemy
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr

from app.core.database import Base

# Re-exportar Base para que otros modelos la usen
__all__ = ["Base", "TimestampMixin", "SoftDeleteMixin"]


class TimestampMixin:
    """
    Mixin que agrega campos de timestamp automáticos.
    
    Campos:
    - fecha_creacion: Timestamp de creación (automático)
    - fecha_actualizacion: Timestamp de última actualización (automático)
    """
    
    @declared_attr
    def fecha_creacion(cls):
        return Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
            comment="Fecha y hora de creación del registro"
        )
    
    @declared_attr
    def fecha_actualizacion(cls):
        return Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False,
            comment="Fecha y hora de última actualización"
        )


class SoftDeleteMixin:
    """
    Mixin para soft delete (eliminación lógica).
    
    Campos:
    - fecha_eliminacion: Timestamp de eliminación (NULL si no está eliminado)
    - eliminado: Flag booleano de eliminación
    """
    
    @declared_attr
    def fecha_eliminacion(cls):
        return Column(
            DateTime,
            nullable=True,
            comment="Fecha y hora de eliminación (soft delete)"
        )
    
    @property
    def eliminado(self) -> bool:
        """Verifica si el registro está eliminado"""
        return self.fecha_eliminacion is not None
    
    def soft_delete(self):
        """Marca el registro como eliminado"""
        self.fecha_eliminacion = datetime.utcnow()
    
    def restore(self):
        """Restaura un registro eliminado"""
        self.fecha_eliminacion = None