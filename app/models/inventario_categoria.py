"""Modelo InventarioCategoria"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class InventarioCategoria(Base):
    __tablename__ = "inventario_categorias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    
    gimnasio = relationship("Gimnasio", back_populates="inventario_categorias")
    items = relationship("Inventario", back_populates="categoria")
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "descripcion": self.descripcion}