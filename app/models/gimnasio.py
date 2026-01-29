"""
Modelo Gimnasio
Representa un gimnasio en el sistema multi-tenant
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base, TimestampMixin


class Gimnasio(Base, TimestampMixin):
    """
    Modelo de Gimnasio.
    
    Un gimnasio es la entidad principal del sistema multi-tenant.
    Cada gimnasio tiene sus propios usuarios, membresías, clases, etc.
    """
    
    __tablename__ = "gimnasios"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, comment="Nombre del gimnasio")
    descripcion = Column(Text, nullable=True, comment="Descripción del gimnasio")
    direccion = Column(String(300), nullable=True, comment="Dirección física")
    telefono = Column(String(20), nullable=True, comment="Teléfono de contacto")
    email = Column(String(150), unique=True, nullable=False, index=True, comment="Email del gimnasio")
    logo_url = Column(String(500), nullable=True, comment="URL del logo")
    codigo_unico = Column(String(50), unique=True, nullable=False, index=True, comment="Código único del gimnasio")
    activo = Column(Boolean, default=True, nullable=False, comment="Si el gimnasio está activo")
    
    # Relaciones
    usuarios = relationship("Usuario", back_populates="gimnasio", cascade="all, delete-orphan")
    membresias_tipos = relationship("MembresiaTipo", back_populates="gimnasio", cascade="all, delete-orphan")
    accesos = relationship("Acceso", back_populates="gimnasio", cascade="all, delete-orphan")
    clases = relationship("Clase", back_populates="gimnasio", cascade="all, delete-orphan")
    productos_categorias = relationship("ProductoCategoria", back_populates="gimnasio", cascade="all, delete-orphan")
    productos = relationship("Producto", back_populates="gimnasio", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="gimnasio", cascade="all, delete-orphan")
    inventario_categorias = relationship("InventarioCategoria", back_populates="gimnasio", cascade="all, delete-orphan")
    inventario = relationship("Inventario", back_populates="gimnasio", cascade="all, delete-orphan")
    rutinas = relationship("Rutina", back_populates="gimnasio", cascade="all, delete-orphan")
    logs_actividad = relationship("LogActividad", back_populates="gimnasio", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Gimnasio(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo_unico}')>"
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email,
            "logo_url": self.logo_url,
            "codigo_unico": self.codigo_unico,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }