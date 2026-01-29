"""Modelo Notificacion"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.core.constants import TipoNotificacionEnum

class Notificacion(Base):
    __tablename__ = "notificaciones"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo = Column(SQLEnum(TipoNotificacionEnum), nullable=False)
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_lectura = Column(DateTime, nullable=True)
    
    usuario = relationship("Usuario", back_populates="notificaciones")
    
    def to_dict(self):
        return {"id": self.id, "tipo": self.tipo.value if self.tipo else None, "titulo": self.titulo, "leida": self.leida}