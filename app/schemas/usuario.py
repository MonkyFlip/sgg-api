"""Schemas de Usuario"""
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.core.constants import GeneroEnum

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str | None = Field(None, max_length=20)
    fecha_nacimiento: date | None = None
    genero: GeneroEnum | None = None
    direccion: str | None = Field(None, max_length=300)
    documento_identidad: str | None = Field(None, max_length=50)

class UsuarioCreate(UsuarioBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=8)
    rol_id: int
    gimnasio_id: int | None = None

class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario"""
    nombre: str | None = Field(None, min_length=2, max_length=100)
    apellido: str | None = Field(None, min_length=2, max_length=100)
    telefono: str | None = None
    fecha_nacimiento: date | None = None
    genero: GeneroEnum | None = None
    foto_perfil_url: str | None = None
    direccion: str | None = None
    documento_identidad: str | None = None
    activo: bool | None = None

class UsuarioResponse(UsuarioBase):
    """Schema de respuesta de usuario"""
    id: int
    gimnasio_id: int
    rol_id: int
    rol_nombre: str | None = None
    nombre_completo: str | None = None
    edad: int | None = None
    foto_perfil_url: str | None = None
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UsuarioDetail(UsuarioResponse):
    """Schema detallado de usuario con relaciones"""
    pass