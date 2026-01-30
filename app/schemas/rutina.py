"""Schemas de Rutina"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import NivelEntrenamientoEnum, TipoRutinaEnum

class RutinaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = None
    objetivo: str | None = Field(None, max_length=255)
    nivel: NivelEntrenamientoEnum
    tipo: TipoRutinaEnum
    duracion_semanas: int | None = Field(None, gt=0)

class RutinaCreate(RutinaBase):
    """Schema para crear rutina"""
    gimnasio_id: int
    creador_id: int
    cliente_id: int | None = None

class RutinaUpdate(BaseModel):
    """Schema para actualizar rutina"""
    nombre: str | None = None
    descripcion: str | None = None
    objetivo: str | None = None
    nivel: NivelEntrenamientoEnum | None = None
    tipo: TipoRutinaEnum | None = None
    duracion_semanas: int | None = None
    activo: bool | None = None

class RutinaResponse(RutinaBase):
    """Schema de respuesta de rutina"""
    id: int
    gimnasio_id: int
    creador_id: int
    cliente_id: int | None = None
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)