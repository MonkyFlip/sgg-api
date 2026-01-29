"""
Modelo MembresiaTipo
Representa los tipos de membresías disponibles en cada gimnasio
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class MembresiaTipo(Base):
    """
    Modelo de Tipo de Membresía.
    
    Define los diferentes tipos de membresías que ofrece un gimnasio
    (mensual, trimestral, anual, etc.)
    """
    
    __tablename__ = "membresias_tipos"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    nombre = Column(String(100), nullable=False, comment="Nombre del tipo de membresía")
    descripcion = Column(Text, nullable=True, comment="Descripción de la membresía")
    precio = Column(Numeric(10, 2), nullable=False, comment="Precio de la membresía")
    duracion_dias = Column(Integer, nullable=False, comment="Duración en días")
    beneficios = Column(JSON, nullable=True, comment="Lista de beneficios incluidos")
    activo = Column(Boolean, default=True, nullable=False, comment="Si está disponible para venta")
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    gimnasio = relationship("Gimnasio", back_populates="membresias_tipos")
    membresias = relationship("Membresia", back_populates="membresia_tipo")
    
    def __repr__(self):
        return f"<MembresiaTipo(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "gimnasio_id": self.gimnasio_id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio) if self.precio else None,
            "duracion_dias": self.duracion_dias,
            "beneficios": self.beneficios,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }