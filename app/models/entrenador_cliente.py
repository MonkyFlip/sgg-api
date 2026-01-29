"""
Modelo EntrenadorCliente
Relación entre entrenadores y sus clientes asignados
"""

from sqlalchemy import Column, Integer, Date, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class EntrenadorCliente(Base):
    """
    Modelo de relación Entrenador-Cliente.
    
    Representa la asignación de un cliente a un entrenador personal.
    """
    
    __tablename__ = "entrenadores_clientes"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entrenador_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    fecha_asignacion = Column(Date, nullable=False, comment="Fecha de asignación")
    fecha_finalizacion = Column(Date, nullable=True, comment="Fecha de finalización")
    activo = Column(Boolean, default=True, nullable=False, comment="Si la asignación está activa")
    notas = Column(Text, nullable=True, comment="Notas sobre la relación")
    
    # Relaciones
    entrenador = relationship("Usuario", back_populates="clientes_asignados", foreign_keys=[entrenador_id])
    cliente = relationship("Usuario", back_populates="entrenador_asignado", foreign_keys=[cliente_id])
    
    def __repr__(self):
        return f"<EntrenadorCliente(entrenador_id={self.entrenador_id}, cliente_id={self.cliente_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "entrenador_id": self.entrenador_id,
            "cliente_id": self.cliente_id,
            "fecha_asignacion": self.fecha_asignacion.isoformat() if self.fecha_asignacion else None,
            "fecha_finalizacion": self.fecha_finalizacion.isoformat() if self.fecha_finalizacion else None,
            "activo": self.activo,
            "notas": self.notas,
        }