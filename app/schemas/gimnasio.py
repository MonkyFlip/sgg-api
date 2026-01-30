"""Schemas de Gimnasio"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class GimnasioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=200)
    descripcion: str | None = None
    direccion: str | None = Field(None, max_length=300)
    telefono: str | None = Field(None, max_length=20)
    email: EmailStr
    logo_url: str | None = None

class GimnasioCreate(GimnasioBase):
    """Schema para crear gimnasio"""
    codigo_unico: str = Field(..., min_length=3, max_length=50)

class GimnasioUpdate(BaseModel):
    """Schema para actualizar gimnasio"""
    nombre: str | None = Field(None, min_length=2, max_length=200)
    descripcion: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None
    logo_url: str | None = None
    activo: bool | None = None

class GimnasioResponse(GimnasioBase):
    """Schema de respuesta de gimnasio"""
    id: int
    codigo_unico: str
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)