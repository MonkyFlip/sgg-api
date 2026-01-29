"""Modelo Inventario"""
from sqlalchemy import Column, Integer, String, Text, Date, Numeric, ForeignKey, Boolean, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base, TimestampMixin
from app.core.constants import EstadoEquipamientoEnum

class Inventario(Base, TimestampMixin):
    __tablename__ = "inventario"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("inventario_categorias.id"), nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    codigo = Column(String(50), nullable=True)
    cantidad = Column(Integer, default=1, nullable=False)
    estado = Column(SQLEnum(EstadoEquipamientoEnum), default=EstadoEquipamientoEnum.BUENO, nullable=False)
    fecha_adquisicion = Column(Date, nullable=True)
    costo = Column(Numeric(10, 2), nullable=True)
    ubicacion = Column(String(200), nullable=True)
    fecha_ultimo_mantenimiento = Column(Date, nullable=True)
    fecha_proximo_mantenimiento = Column(Date, nullable=True)
    activo = Column(Boolean, default=True, nullable=False)
    
    gimnasio = relationship("Gimnasio", back_populates="inventario")
    categoria = relationship("InventarioCategoria", back_populates="items")
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "cantidad": self.cantidad, "estado": self.estado.value if self.estado else None}