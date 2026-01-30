"""Schemas de Categoría de Inventario"""
from pydantic import BaseModel, Field, ConfigDict

class InventarioCategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str | None = None

class InventarioCategoriaCreate(InventarioCategoriaBase):
    """Schema para crear categoría"""
    gimnasio_id: int

class InventarioCategoriaUpdate(BaseModel):
    """Schema para actualizar categoría"""
    nombre: str | None = None
    descripcion: str | None = None

class InventarioCategoriaResponse(InventarioCategoriaBase):
    """Schema de respuesta de categoría"""
    id: int
    gimnasio_id: int
    
    model_config = ConfigDict(from_attributes=True)