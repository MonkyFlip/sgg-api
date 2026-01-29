"""Modelo RutinaEjercicio"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.core.constants import DiaSemanaEnum

class RutinaEjercicio(Base):
    __tablename__ = "rutinas_ejercicios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rutina_id = Column(Integer, ForeignKey("rutinas.id", ondelete="CASCADE"), nullable=False, index=True)
    dia_semana = Column(SQLEnum(DiaSemanaEnum), nullable=False)
    orden = Column(Integer, nullable=False)
    nombre_ejercicio = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    series = Column(Integer, nullable=False)
    repeticiones = Column(String(50), nullable=False)
    peso = Column(String(50), nullable=True)
    descanso_segundos = Column(Integer, nullable=True)
    notas = Column(Text, nullable=True)
    video_url = Column(String(500), nullable=True)
    
    rutina = relationship("Rutina", back_populates="ejercicios")
    
    def to_dict(self):
        return {"id": self.id, "nombre_ejercicio": self.nombre_ejercicio, "series": self.series, "repeticiones": self.repeticiones}