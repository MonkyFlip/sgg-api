"""Modelo FacturaDetalle"""
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.core.constants import TipoItemFacturaEnum

class FacturaDetalle(Base):
    __tablename__ = "facturas_detalle"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    factura_id = Column(Integer, ForeignKey("facturas.id", ondelete="CASCADE"), nullable=False, index=True)
    concepto = Column(String(255), nullable=False)
    tipo_item = Column(SQLEnum(TipoItemFacturaEnum), nullable=False)
    item_id = Column(Integer, nullable=True)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    factura = relationship("Factura", back_populates="detalles")
    
    def to_dict(self):
        return {"id": self.id, "concepto": self.concepto, "cantidad": self.cantidad, "subtotal": float(self.subtotal) if self.subtotal else None}