"""Schemas de Pago"""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import MetodoPagoEnum

class PagoCreate(BaseModel):
    """Schema para crear pago"""
    factura_id: int
    monto: Decimal = Field(..., gt=0, decimal_places=2)
    metodo_pago: MetodoPagoEnum
    referencia: str | None = Field(None, max_length=100)
    notas: str | None = None

class PagoResponse(BaseModel):
    """Schema de respuesta de pago"""
    id: int
    factura_id: int
    monto: Decimal
    metodo_pago: MetodoPagoEnum
    referencia: str | None = None
    fecha_pago: datetime
    notas: str | None = None
    
    model_config = ConfigDict(from_attributes=True)