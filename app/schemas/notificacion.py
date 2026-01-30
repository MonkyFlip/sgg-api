"""Schemas de Notificación"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import TipoNotificacionEnum

class NotificacionBase(BaseModel):
    tipo: TipoNotificacionEnum
    titulo: str = Field(..., min_length=2, max_length=200)
    mensaje: str = Field(..., min_length=5)

class NotificacionCreate(NotificacionBase):
    """Schema para crear notificación"""
    usuario_id: int

class NotificacionUpdate(BaseModel):
    """Schema para actualizar notificación"""
    leida: bool

class NotificacionResponse(NotificacionBase):
    """Schema de respuesta de notificación"""
    id: int
    usuario_id: int
    leida: bool
    fecha_creacion: datetime
    fecha_lectura: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)