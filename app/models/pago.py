"""Modelo Pago"""
from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
from app.core.constants import MetodoPagoEnum

class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    factura_id = Column(Integer, ForeignKey("facturas.id", ondelete="CASCADE"), nullable=False, index=True)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(SQLEnum(MetodoPagoEnum), nullable=False)
    referencia = Column(String(100), nullable=True)
    fecha_pago = Column(DateTime, default=datetime.utcnow, nullable=False)
    notas = Column(Text, nullable=True)
    
    factura = relationship("Factura", back_populates="pagos")
    
    def to_dict(self):
        return {"id": self.id, "monto": float(self.monto) if self.monto else None, "metodo_pago": self.metodo_pago.value if self.metodo_pago else None}