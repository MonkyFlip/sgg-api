"""
Modelo ClaseHorario
Horarios específicos de cada clase
"""

from sqlalchemy import Column, Integer, Time, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.core.constants import DiaSemanaEnum


class ClaseHorario(Base):
    """Modelo de Horario de Clase"""
    
    __tablename__ = "clases_horarios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    clase_id = Column(Integer, ForeignKey("clases.id", ondelete="CASCADE"), nullable=False, index=True)
    dia_semana = Column(SQLEnum(DiaSemanaEnum), nullable=False, comment="Día de la semana")
    hora_inicio = Column(Time, nullable=False, comment="Hora de inicio")
    hora_fin = Column(Time, nullable=False, comment="Hora de fin")
    activo = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    clase = relationship("Clase", back_populates="horarios")
    reservas = relationship("Reserva", back_populates="clase_horario", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ClaseHorario(id={self.id}, clase_id={self.clase_id}, dia='{self.dia_semana}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "clase_id": self.clase_id,
            "dia_semana": self.dia_semana.value if self.dia_semana else None,
            "hora_inicio": str(self.hora_inicio) if self.hora_inicio else None,
            "hora_fin": str(self.hora_fin) if self.hora_fin else None,
            "activo": self.activo,
        }