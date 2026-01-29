"""
Modelo Membresia
Representa las membresías activas/históricas de los clientes
"""

from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date

from app.models.base import Base, TimestampMixin
from app.core.constants import EstadoMembresiaEnum


class Membresia(Base, TimestampMixin):
    """
    Modelo de Membresía.
    
    Representa una membresía activa o histórica de un cliente.
    """
    
    __tablename__ = "membresias"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    membresia_tipo_id = Column(Integer, ForeignKey("membresias_tipos.id"), nullable=False, index=True)
    
    fecha_inicio = Column(Date, nullable=False, comment="Fecha de inicio de la membresía")
    fecha_fin = Column(Date, nullable=False, comment="Fecha de fin de la membresía")
    estado = Column(
        SQLEnum(EstadoMembresiaEnum),
        default=EstadoMembresiaEnum.ACTIVA,
        nullable=False,
        index=True,
        comment="Estado de la membresía"
    )
    precio_pagado = Column(Numeric(10, 2), nullable=False, comment="Precio que se pagó")
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="membresias")
    membresia_tipo = relationship("MembresiaTipo", back_populates="membresias")
    
    def __repr__(self):
        return f"<Membresia(id={self.id}, usuario_id={self.usuario_id}, estado='{self.estado}')>"
    
    @property
    def esta_activa(self) -> bool:
        """Verifica si la membresía está activa y vigente"""
        return (
            self.estado == EstadoMembresiaEnum.ACTIVA and
            self.fecha_inicio <= date.today() <= self.fecha_fin
        )
    
    @property
    def dias_restantes(self) -> int:
        """Calcula los días restantes de la membresía"""
        if self.fecha_fin < date.today():
            return 0
        return (self.fecha_fin - date.today()).days
    
    @property
    def dias_totales(self) -> int:
        """Calcula los días totales de la membresía"""
        return (self.fecha_fin - self.fecha_inicio).days
    
    @property
    def dias_usados(self) -> int:
        """Calcula los días que ya ha usado de la membresía"""
        if date.today() < self.fecha_inicio:
            return 0
        if date.today() > self.fecha_fin:
            return self.dias_totales
        return (date.today() - self.fecha_inicio).days
    
    @property
    def porcentaje_usado(self) -> float:
        """Calcula el porcentaje usado de la membresía"""
        if self.dias_totales == 0:
            return 0
        return (self.dias_usados / self.dias_totales) * 100
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "membresia_tipo_id": self.membresia_tipo_id,
            "membresia_tipo_nombre": self.membresia_tipo.nombre if self.membresia_tipo else None,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "estado": self.estado.value if self.estado else None,
            "precio_pagado": float(self.precio_pagado) if self.precio_pagado else None,
            "esta_activa": self.esta_activa,
            "dias_restantes": self.dias_restantes,
            "dias_totales": self.dias_totales,
            "dias_usados": self.dias_usados,
            "porcentaje_usado": round(self.porcentaje_usado, 2),
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }
    
    def activar(self):
        """Activa la membresía"""
        self.estado = EstadoMembresiaEnum.ACTIVA
    
    def cancelar(self):
        """Cancela la membresía"""
        self.estado = EstadoMembresiaEnum.CANCELADA
    
    def suspender(self):
        """Suspende la membresía"""
        self.estado = EstadoMembresiaEnum.SUSPENDIDA
    
    def marcar_vencida(self):
        """Marca la membresía como vencida"""
        self.estado = EstadoMembresiaEnum.VENCIDA