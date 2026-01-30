"""Schemas de Inventario"""
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.core.constants import EstadoEquipamientoEnum

class InventarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = None
    codigo: str | None = Field(None, max_length=50)
    cantidad: int = Field(default=1, gt=0)
    estado: EstadoEquipamientoEnum = EstadoEquipamientoEnum.BUENO
    fecha_adquisicion: date | None = None
    costo: Decimal | None = Field(None, decimal_places=2)
    ubicacion: str | None = Field(None, max_length=200)
    fecha_ultimo_mantenimiento: date | None = None
    fecha_proximo_mantenimiento: date | None = None

class InventarioCreate(InventarioBase):
    """Schema para crear item de inventario"""
    gimnasio_id: int
    categoria_id: int

class InventarioUpdate(BaseModel):
    """Schema para actualizar inventario"""
    nombre: str | None = None
    descripcion: str | None = None
    codigo: str | None = None
    cantidad: int | None = None
    estado: EstadoEquipamientoEnum | None = None
    fecha_adquisicion: date | None = None
    costo: Decimal | None = None
    ubicacion: str | None = None
    fecha_ultimo_mantenimiento: date | None = None
    fecha_proximo_mantenimiento: date | None = None
    activo: bool | None = None

class InventarioResponse(InventarioBase):
    """Schema de respuesta de inventario"""
    id: int
    gimnasio_id: int
    categoria_id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)