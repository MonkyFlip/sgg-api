"""Schemas de Horario de Clase"""
from datetime import time
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import DiaSemanaEnum

class ClaseHorarioBase(BaseModel):
    dia_semana: DiaSemanaEnum
    hora_inicio: time
    hora_fin: time

class ClaseHorarioCreate(ClaseHorarioBase):
    """Schema para crear horario"""
    clase_id: int

class ClaseHorarioUpdate(BaseModel):
    """Schema para actualizar horario"""
    dia_semana: DiaSemanaEnum | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    activo: bool | None = None

class ClaseHorarioResponse(ClaseHorarioBase):
    """Schema de respuesta de horario"""
    id: int
    clase_id: int
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)