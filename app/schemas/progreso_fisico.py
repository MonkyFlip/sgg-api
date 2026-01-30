"""Schemas de Progreso Físico"""
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProgresoFisicoBase(BaseModel):
    fecha_registro: date
    peso: Decimal | None = Field(None, ge=0, decimal_places=2)
    altura: Decimal | None = Field(None, ge=0, decimal_places=2)
    imc: Decimal | None = Field(None, ge=0, decimal_places=2)
    porcentaje_grasa: Decimal | None = Field(None, ge=0, le=100, decimal_places=2)
    masa_muscular: Decimal | None = Field(None, ge=0, decimal_places=2)
    circunferencia_pecho: Decimal | None = Field(None, ge=0, decimal_places=2)
    circunferencia_cintura: Decimal | None = Field(None, ge=0, decimal_places=2)
    circunferencia_cadera: Decimal | None = Field(None, ge=0, decimal_places=2)
    circunferencia_brazo: Decimal | None = Field(None, ge=0, decimal_places=2)
    circunferencia_pierna: Decimal | None = Field(None, ge=0, decimal_places=2)
    foto_frontal_url: str | None = None
    foto_lateral_url: str | None = None
    foto_posterior_url: str | None = None
    notas: str | None = None

class ProgresoFisicoCreate(ProgresoFisicoBase):
    """Schema para crear progreso físico"""
    usuario_id: int

class ProgresoFisicoUpdate(BaseModel):
    """Schema para actualizar progreso físico"""
    peso: Decimal | None = None
    altura: Decimal | None = None
    imc: Decimal | None = None
    porcentaje_grasa: Decimal | None = None
    masa_muscular: Decimal | None = None
    circunferencia_pecho: Decimal | None = None
    circunferencia_cintura: Decimal | None = None
    circunferencia_cadera: Decimal | None = None
    circunferencia_brazo: Decimal | None = None
    circunferencia_pierna: Decimal | None = None
    foto_frontal_url: str | None = None
    foto_lateral_url: str | None = None
    foto_posterior_url: str | None = None
    notas: str | None = None

class ProgresoFisicoResponse(ProgresoFisicoBase):
    """Schema de respuesta de progreso físico"""
    id: int
    usuario_id: int
    fecha_creacion: datetime
    
    model_config = ConfigDict(from_attributes=True)