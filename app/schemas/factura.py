"""Schemas de Factura"""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import TipoFacturaEnum, EstadoFacturaEnum, MetodoPagoEnum

class FacturaDetalleCreate(BaseModel):
    """Schema para crear detalle de factura"""
    concepto: str = Field(..., min_length=2, max_length=255)
    tipo_item: str
    item_id: int | None = None
    cantidad: int = Field(default=1, gt=0)
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2)

class FacturaCreate(BaseModel):
    """Schema para crear factura"""
    usuario_id: int
    gimnasio_id: int
    tipo: TipoFacturaEnum
    metodo_pago: MetodoPagoEnum | None = None
    notas: str | None = None
    detalles: list[FacturaDetalleCreate]

class FacturaDetalleResponse(BaseModel):
    """Schema de respuesta de detalle"""
    id: int
    factura_id: int
    concepto: str
    tipo_item: str
    item_id: int | None = None
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    
    model_config = ConfigDict(from_attributes=True)

class FacturaResponse(BaseModel):
    """Schema de respuesta de factura"""
    id: int
    gimnasio_id: int
    usuario_id: int
    numero_factura: str
    tipo: TipoFacturaEnum
    subtotal: Decimal
    impuestos: Decimal
    descuentos: Decimal
    total: Decimal
    estado: EstadoFacturaEnum
    metodo_pago: MetodoPagoEnum | None = None
    notas: str | None = None
    fecha_emision: datetime
    fecha_pago: datetime | None = None
    detalles: list[FacturaDetalleResponse] | None = None
    
    model_config = ConfigDict(from_attributes=True)