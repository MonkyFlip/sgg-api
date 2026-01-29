"""Modelo Dieta"""
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin

class Dieta(Base, TimestampMixin):
    __tablename__ = "dietas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entrenador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    objetivo = Column(String(255), nullable=True)
    calorias_totales = Column(Integer, nullable=True)
    proteinas_gramos = Column(Numeric(6, 2), nullable=True)
    carbohidratos_gramos = Column(Numeric(6, 2), nullable=True)
    grasas_gramos = Column(Numeric(6, 2), nullable=True)
    descripcion = Column(Text, nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    entrenador = relationship("Usuario", back_populates="dietas_creadas", foreign_keys=[entrenador_id])
    cliente = relationship("Usuario", back_populates="dietas_asignadas", foreign_keys=[cliente_id])
    comidas = relationship("DietaComida", back_populates="dieta", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "calorias_totales": self.calorias_totales}