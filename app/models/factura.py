"""Modelo Factura"""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum as SQLEnum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.core.constants import TipoFacturaEnum, EstadoFacturaEnum, MetodoPagoEnum

class Factura(Base):
    __tablename__ = "facturas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    tipo = Column(SQLEnum(TipoFacturaEnum), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    impuestos = Column(Numeric(10, 2), default=0)
    descuentos = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(SQLEnum(EstadoFacturaEnum), default=EstadoFacturaEnum.PENDIENTE, nullable=False)
    metodo_pago = Column(SQLEnum(MetodoPagoEnum), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_emision = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_pago = Column(DateTime, nullable=True)
    
    gimnasio = relationship("Gimnasio", back_populates="facturas")
    usuario = relationship("Usuario", back_populates="facturas")
    detalles = relationship("FacturaDetalle", back_populates="factura", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="factura", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {"id": self.id, "numero_factura": self.numero_factura, "total": float(self.total) if self.total else None, "estado": self.estado.value if self.estado else None}