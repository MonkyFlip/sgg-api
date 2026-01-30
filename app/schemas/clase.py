"""Schemas de Clase"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ClaseBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150)
    descripcion: str | None = None
    capacidad_maxima: int = Field(..., gt=0)
    duracion_minutos: int = Field(..., gt=0)

class ClaseCreate(ClaseBase):
    """Schema para crear clase"""
    gimnasio_id: int
    entrenador_id: int

class ClaseUpdate(BaseModel):
    """Schema para actualizar clase"""
    nombre: str | None = None
    descripcion: str | None = None
    capacidad_maxima: int | None = None
    duracion_minutos: int | None = None
    entrenador_id: int | None = None
    activo: bool | None = None

class ClaseResponse(ClaseBase):
    """Schema de respuesta de clase"""
    id: int
    gimnasio_id: int
    entrenador_id: int
    entrenador_nombre: str | None = None
    activo: bool
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)