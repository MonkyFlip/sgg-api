"""Schemas de Entrenador-Cliente"""
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

class EntrenadorClienteBase(BaseModel):
    fecha_asignacion: date
    notas: str | None = None

class EntrenadorClienteCreate(EntrenadorClienteBase):
    """Schema para crear relación entrenador-cliente"""
    entrenador_id: int
    cliente_id: int

class EntrenadorClienteUpdate(BaseModel):
    """Schema para actualizar relación"""
    fecha_finalizacion: date | None = None
    activo: bool | None = None
    notas: str | None = None

class EntrenadorClienteResponse(EntrenadorClienteBase):
    """Schema de respuesta"""
    id: int
    entrenador_id: int
    cliente_id: int
    fecha_finalizacion: date | None = None
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)