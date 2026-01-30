"""Schemas de Acceso"""
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import TipoAccesoEnum

class AccesoBase(BaseModel):
    notas: str | None = None

class AccesoCreate(AccesoBase):
    """Schema para crear acceso"""
    usuario_id: int
    gimnasio_id: int
    tipo_acceso: TipoAccesoEnum

class RegistrarEntrada(BaseModel):
    """Schema para registrar entrada"""
    usuario_id: int
    tipo_acceso: TipoAccesoEnum = TipoAccesoEnum.ENTRADA

class RegistrarSalida(BaseModel):
    """Schema para registrar salida"""
    usuario_id: int

class AccesoResponse(AccesoBase):
    """Schema de respuesta de acceso"""
    id: int
    usuario_id: int
    gimnasio_id: int
    fecha_hora_entrada: datetime
    fecha_hora_salida: datetime | None = None
    tipo_acceso: TipoAccesoEnum
    duracion_minutos: int | None = None
    
    model_config = ConfigDict(from_attributes=True)