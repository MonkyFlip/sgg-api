"""
Modelo Clase
Representa las clases grupales disponibles
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base


class Clase(Base):
    """
    Modelo de Clase Grupal.
    
    Define las clases grupales que ofrece el gimnasio (Yoga, Spinning, CrossFit, etc.)
    """
    
    __tablename__ = "clases"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    entrenador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    nombre = Column(String(150), nullable=False, comment="Nombre de la clase")
    descripcion = Column(Text, nullable=True, comment="Descripción de la clase")
    capacidad_maxima = Column(Integer, nullable=False, comment="Capacidad máxima de participantes")
    duracion_minutos = Column(Integer, nullable=False, comment="Duración en minutos")
    activo = Column(Boolean, default=True, nullable=False, comment="Si la clase está disponible")
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones
    gimnasio = relationship("Gimnasio", back_populates="clases")
    entrenador = relationship("Usuario", back_populates="clases_impartidas", foreign_keys=[entrenador_id])
    horarios = relationship("ClaseHorario", back_populates="clase", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Clase(id={self.id}, nombre='{self.nombre}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "gimnasio_id": self.gimnasio_id,
            "entrenador_id": self.entrenador_id,
            "entrenador_nombre": self.entrenador.nombre_completo if self.entrenador else None,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "capacidad_maxima": self.capacidad_maxima,
            "duracion_minutos": self.duracion_minutos,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
        }