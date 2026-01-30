"""Schemas de Tipo de Membresía"""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class MembresiaTipoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str | None = None
    precio: Decimal = Field(..., gt=0, decimal_places=2)
    duracion_dias: int = Field(..., gt=0, le=730)
    beneficios: list | None = None

class MembresiaTipoCreate(MembresiaTipoBase):
    """Schema para crear tipo de membresía"""
    gimnasio_id: int

class MembresiaTipoUpdate(BaseModel):
    """Schema para actualizar tipo de membresía"""
    nombre: str | None = None
    descripcion: str | None = None
    precio: Decimal | None = None
    duracion_dias: int | None = None
    beneficios: list | None = None
    activo: bool | None = None

class MembresiaTipoResponse(MembresiaTipoBase):
    """Schema de respuesta de tipo de membresía"""
    id: int
    gimnasio_id: int
    activo: bool
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)