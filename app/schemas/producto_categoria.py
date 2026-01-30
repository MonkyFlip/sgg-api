"""Schemas de Categoría de Producto"""
from pydantic import BaseModel, Field, ConfigDict

class ProductoCategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: str | None = None

class ProductoCategoriaCreate(ProductoCategoriaBase):
    """Schema para crear categoría"""
    gimnasio_id: int

class ProductoCategoriaUpdate(BaseModel):
    """Schema para actualizar categoría"""
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None

class ProductoCategoriaResponse(ProductoCategoriaBase):
    """Schema de respuesta de categoría"""
    id: int
    gimnasio_id: int
    activo: bool
    
    model_config = ConfigDict(from_attributes=True)