"""Modelo ProgresoFisico"""
from sqlalchemy import Column, Integer, Date, Text, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class ProgresoFisico(Base):
    __tablename__ = "progreso_fisico"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha_registro = Column(Date, nullable=False, index=True)
    peso = Column(Numeric(5, 2), nullable=True)
    altura = Column(Numeric(5, 2), nullable=True)
    imc = Column(Numeric(5, 2), nullable=True)
    porcentaje_grasa = Column(Numeric(5, 2), nullable=True)
    masa_muscular = Column(Numeric(5, 2), nullable=True)
    circunferencia_pecho = Column(Numeric(5, 2), nullable=True)
    circunferencia_cintura = Column(Numeric(5, 2), nullable=True)
    circunferencia_cadera = Column(Numeric(5, 2), nullable=True)
    circunferencia_brazo = Column(Numeric(5, 2), nullable=True)
    circunferencia_pierna = Column(Numeric(5, 2), nullable=True)
    foto_frontal_url = Column(String(500), nullable=True)
    foto_lateral_url = Column(String(500), nullable=True)
    foto_posterior_url = Column(String(500), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    usuario = relationship("Usuario", back_populates="progreso_fisico")
    
    def to_dict(self):
        return {"id": self.id, "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None, "peso": float(self.peso) if self.peso else None, "imc": float(self.imc) if self.imc else None}