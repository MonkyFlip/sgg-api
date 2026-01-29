"""
Modelo Acceso
Registra las entradas y salidas de los usuarios al gimnasio
"""

from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.core.constants import TipoAccesoEnum


class Acceso(Base):
    """
    Modelo de Acceso.
    
    Registra cuando un usuario entra o sale del gimnasio.
    """
    
    __tablename__ = "accesos"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    fecha_hora_entrada = Column(DateTime, nullable=False, index=True, comment="Fecha y hora de entrada")
    fecha_hora_salida = Column(DateTime, nullable=True, comment="Fecha y hora de salida")
    tipo_acceso = Column(SQLEnum(TipoAccesoEnum), nullable=False, comment="Tipo de acceso")
    notas = Column(Text, nullable=True, comment="Notas adicionales")
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="accesos")
    gimnasio = relationship("Gimnasio", back_populates="accesos")
    
    def __repr__(self):
        return f"<Acceso(id={self.id}, usuario_id={self.usuario_id}, tipo='{self.tipo_acceso}')>"
    
    @property
    def duracion_minutos(self) -> int:
        """Calcula la duración de la visita en minutos"""
        if not self.fecha_hora_salida:
            return None
        duracion = self.fecha_hora_salida - self.fecha_hora_entrada
        return int(duracion.total_seconds() / 60)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "gimnasio_id": self.gimnasio_id,
            "fecha_hora_entrada": self.fecha_hora_entrada.isoformat() if self.fecha_hora_entrada else None,
            "fecha_hora_salida": self.fecha_hora_salida.isoformat() if self.fecha_hora_salida else None,
            "tipo_acceso": self.tipo_acceso.value if self.tipo_acceso else None,
            "duracion_minutos": self.duracion_minutos,
            "notas": self.notas,
        }