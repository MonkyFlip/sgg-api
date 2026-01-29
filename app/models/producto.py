"""Modelo Producto"""
from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin

class Producto(Base, TimestampMixin):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("productos_categorias.id"), nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)
    stock_minimo = Column(Integer, default=0, nullable=False)
    imagen_url = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    gimnasio = relationship("Gimnasio", back_populates="productos")
    categoria = relationship("ProductoCategoria", back_populates="productos")
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "precio": float(self.precio) if self.precio else None, "stock_actual": self.stock_actual}