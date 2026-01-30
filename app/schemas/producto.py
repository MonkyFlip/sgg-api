"""Schemas de Producto"""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = None
    precio: Decimal = Field(..., gt=0, decimal_places=2)
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    imagen_url: str | None = None

class ProductoCreate(ProductoBase):
    """Schema para crear producto"""
    gimnasio_id: int
    categoria_id: int

class ProductoUpdate(BaseModel):
    """Schema para actualizar producto"""
    nombre: str | None = None
    descripcion: str | None = None
    precio: Decimal | None = None
    stock_actual: int | None = None
    stock_minimo: int | None = None
    imagen_url: str | None = None
    activo: bool | None = None

class ProductoResponse(ProductoBase):
    """Schema de respuesta de producto"""
    id: int
    gimnasio_id: int
    categoria_id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)