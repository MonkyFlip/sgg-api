"""Schemas de Reserva"""
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import EstadoReservaEnum

class ReservaBase(BaseModel):
    fecha_reserva: date

class ReservaCreate(ReservaBase):
    """Schema para crear reserva"""
    usuario_id: int
    clase_horario_id: int

class ReservaUpdate(BaseModel):
    """Schema para actualizar reserva"""
    estado: EstadoReservaEnum

class ReservaResponse(ReservaBase):
    """Schema de respuesta de reserva"""
    id: int
    usuario_id: int
    clase_horario_id: int
    estado: EstadoReservaEnum
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)