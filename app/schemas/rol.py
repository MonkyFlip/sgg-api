"""Schemas de Rol"""
from pydantic import BaseModel, Field, ConfigDict

class RolBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: str | None = None
    permisos: dict | None = None

class RolCreate(RolBase):
    """Schema para crear rol"""
    pass

class RolUpdate(BaseModel):
    """Schema para actualizar rol"""
    nombre: str | None = None
    descripcion: str | None = None
    permisos: dict | None = None

class RolResponse(RolBase):
    """Schema de respuesta de rol"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)