"""Modelo ProductoCategoria"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class ProductoCategoria(Base):
    __tablename__ = "productos_categorias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    gimnasio = relationship("Gimnasio", back_populates="productos_categorias")
    productos = relationship("Producto", back_populates="categoria")
    
    def to_dict(self):
        return {"id": self.id, "gimnasio_id": self.gimnasio_id, "nombre": self.nombre, "descripcion": self.descripcion, "activo": self.activo}