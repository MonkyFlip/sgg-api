"""Modelo LogActividad"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class LogActividad(Base):
    __tablename__ = "logs_actividad"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True, index=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    accion = Column(String(255), nullable=False)
    entidad = Column(String(100), nullable=True)
    entidad_id = Column(Integer, nullable=True)
    descripcion = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    usuario = relationship("Usuario", back_populates="logs_actividad")
    gimnasio = relationship("Gimnasio", back_populates="logs_actividad")
    
    def to_dict(self):
        return {"id": self.id, "accion": self.accion, "entidad": self.entidad, "fecha_hora": self.fecha_hora.isoformat() if self.fecha_hora else None}