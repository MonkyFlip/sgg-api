"""Schemas de Ejercicio de Rutina"""
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import DiaSemanaEnum

class RutinaEjercicioBase(BaseModel):
    dia_semana: DiaSemanaEnum
    orden: int = Field(..., ge=1)
    nombre_ejercicio: str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = None
    series: int = Field(..., gt=0)
    repeticiones: str = Field(..., max_length=50)
    peso: str | None = Field(None, max_length=50)
    descanso_segundos: int | None = Field(None, ge=0)
    notas: str | None = None
    video_url: str | None = None

class RutinaEjercicioCreate(RutinaEjercicioBase):
    """Schema para crear ejercicio"""
    rutina_id: int

class RutinaEjercicioUpdate(BaseModel):
    """Schema para actualizar ejercicio"""
    dia_semana: DiaSemanaEnum | None = None
    orden: int | None = None
    nombre_ejercicio: str | None = None
    descripcion: str | None = None
    series: int | None = None
    repeticiones: str | None = None
    peso: str | None = None
    descanso_segundos: int | None = None
    notas: str | None = None
    video_url: str | None = None

class RutinaEjercicioResponse(RutinaEjercicioBase):
    """Schema de respuesta de ejercicio"""
    id: int
    rutina_id: int
    
    model_config = ConfigDict(from_attributes=True)