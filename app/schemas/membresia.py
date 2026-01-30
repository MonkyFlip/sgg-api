"""Schemas de Membresía"""
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import EstadoMembresiaEnum

class MembresiaBase(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    precio_pagado: Decimal = Field(..., gt=0, decimal_places=2)

class MembresiaCreate(MembresiaBase):
    """Schema para crear membresía"""
    usuario_id: int
    membresia_tipo_id: int

class MembresiaUpdate(BaseModel):
    """Schema para actualizar membresía"""
    fecha_fin: date | None = None
    estado: EstadoMembresiaEnum | None = None

class MembresiaResponse(MembresiaBase):
    """Schema de respuesta de membresía"""
    id: int
    usuario_id: int
    membresia_tipo_id: int
    membresia_tipo_nombre: str | None = None
    estado: EstadoMembresiaEnum
    esta_activa: bool | None = None
    dias_restantes: int | None = None
    dias_totales: int | None = None
    dias_usados: int | None = None
    porcentaje_usado: float | None = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)