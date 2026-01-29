"""Modelo DietaComida"""
from sqlalchemy import Column, Integer, Text, Time, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.core.constants import TipoComidaEnum

class DietaComida(Base):
    __tablename__ = "dietas_comidas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dieta_id = Column(Integer, ForeignKey("dietas.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo_comida = Column(SQLEnum(TipoComidaEnum), nullable=False)
    hora_sugerida = Column(Time, nullable=True)
    descripcion = Column(Text, nullable=False)
    calorias = Column(Integer, nullable=True)
    proteinas_gramos = Column(Numeric(6, 2), nullable=True)
    carbohidratos_gramos = Column(Numeric(6, 2), nullable=True)
    grasas_gramos = Column(Numeric(6, 2), nullable=True)
    notas = Column(Text, nullable=True)
    
    dieta = relationship("Dieta", back_populates="comidas")
    
    def to_dict(self):
        return {"id": self.id, "tipo_comida": self.tipo_comida.value if self.tipo_comida else None, "descripcion": self.descripcion}