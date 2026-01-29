"""Modelo Reserva - Reservas de clases"""
from sqlalchemy import Column, Integer, Date, ForeignKey, Enum as SQLEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
from app.core.constants import EstadoReservaEnum

class Reserva(Base, TimestampMixin):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    clase_horario_id = Column(Integer, ForeignKey("clases_horarios.id", ondelete="CASCADE"), nullable=False, index=True)
    fecha_reserva = Column(Date, nullable=False, index=True)
    estado = Column(SQLEnum(EstadoReservaEnum), default=EstadoReservaEnum.CONFIRMADA, nullable=False)
    
    usuario = relationship("Usuario", back_populates="reservas")
    clase_horario = relationship("ClaseHorario", back_populates="reservas")
    
    __table_args__ = (
        UniqueConstraint('usuario_id', 'clase_horario_id', 'fecha_reserva', name='reserva_unica'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "clase_horario_id": self.clase_horario_id,
            "fecha_reserva": self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            "estado": self.estado.value if self.estado else None,
        }