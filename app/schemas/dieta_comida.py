"""Schemas de Comida de Dieta"""
from datetime import time
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import TipoComidaEnum

class DietaComidaBase(BaseModel):
    tipo_comida: TipoComidaEnum
    hora_sugerida: time | None = None
    descripcion: str = Field(..., min_length=5)
    calorias: int | None = Field(None, ge=0)
    proteinas_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    carbohidratos_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    grasas_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    notas: str | None = None

class DietaComidaCreate(DietaComidaBase):
    """Schema para crear comida"""
    dieta_id: int

class DietaComidaUpdate(BaseModel):
    """Schema para actualizar comida"""
    tipo_comida: TipoComidaEnum | None = None
    hora_sugerida: time | None = None
    descripcion: str | None = None
    calorias: int | None = None
    proteinas_gramos: Decimal | None = None
    carbohidratos_gramos: Decimal | None = None
    grasas_gramos: Decimal | None = None
    notas: str | None = None

class DietaComidaResponse(DietaComidaBase):
    """Schema de respuesta de comida"""
    id: int
    dieta_id: int
    
    model_config = ConfigDict(from_attributes=True)