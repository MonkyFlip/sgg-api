"""Schemas de Dieta"""
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class DietaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    objetivo: str | None = Field(None, max_length=255)
    calorias_totales: int | None = Field(None, ge=0)
    proteinas_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    carbohidratos_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    grasas_gramos: Decimal | None = Field(None, ge=0, decimal_places=2)
    descripcion: str | None = None
    fecha_inicio: date
    fecha_fin: date | None = None

class DietaCreate(DietaBase):
    """Schema para crear dieta"""
    entrenador_id: int
    cliente_id: int

class DietaUpdate(BaseModel):
    """Schema para actualizar dieta"""
    nombre: str | None = None
    objetivo: str | None = None
    calorias_totales: int | None = None
    proteinas_gramos: Decimal | None = None
    carbohidratos_gramos: Decimal | None = None
    grasas_gramos: Decimal | None = None
    descripcion: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activo: bool | None = None

class DietaResponse(DietaBase):
    """Schema de respuesta de dieta"""
    id: int
    entrenador_id: int
    cliente_id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)