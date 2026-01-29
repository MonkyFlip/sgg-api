"""Modelo Rutina"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
from app.core.constants import NivelEntrenamientoEnum, TipoRutinaEnum

class Rutina(Base, TimestampMixin):
    __tablename__ = "rutinas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    creador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    objetivo = Column(String(255), nullable=True)
    nivel = Column(SQLEnum(NivelEntrenamientoEnum), nullable=False)
    tipo = Column(SQLEnum(TipoRutinaEnum), nullable=False)
    duracion_semanas = Column(Integer, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    gimnasio = relationship("Gimnasio", back_populates="rutinas")
    creador = relationship("Usuario", back_populates="rutinas_creadas", foreign_keys=[creador_id])
    cliente = relationship("Usuario", back_populates="rutinas_asignadas", foreign_keys=[cliente_id])
    ejercicios = relationship("RutinaEjercicio", back_populates="rutina", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "nivel": self.nivel.value if self.nivel else None, "tipo": self.tipo.value if self.tipo else None}