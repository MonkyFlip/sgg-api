"""Schemas de Autenticación"""
from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """Token de acceso"""
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Datos del token"""
    user_id: int | None = None
    email: str | None = None
    role: str | None = None
    gimnasio_id: int | None = None

class Login(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str = Field(..., min_length=8)

class Register(BaseModel):
    """Schema para registro"""
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    telefono: str | None = None
    gimnasio_codigo: str = Field(..., description="Código del gimnasio")

class PasswordChange(BaseModel):
    """Schema para cambio de contraseña"""
    current_password: str
    new_password: str = Field(..., min_length=8)

class PasswordReset(BaseModel):
    """Schema para reseteo de contraseña"""
    email: EmailStr