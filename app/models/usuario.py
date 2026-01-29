"""
Modelo Usuario
Representa todos los usuarios del sistema (admins, entrenadores, clientes)
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base, TimestampMixin
from app.core.constants import GeneroEnum


class Usuario(Base, TimestampMixin):
    """
    Modelo de Usuario.
    
    Representa a todos los usuarios del sistema independientemente de su rol.
    Cada usuario pertenece a un gimnasio y tiene un rol asignado.
    """
    
    __tablename__ = "usuarios"
    
    # Campos
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    gimnasio_id = Column(Integer, ForeignKey("gimnasios.id", ondelete="CASCADE"), nullable=False, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    
    nombre = Column(String(100), nullable=False, comment="Nombre del usuario")
    apellido = Column(String(100), nullable=False, comment="Apellido del usuario")
    email = Column(String(150), unique=True, nullable=False, index=True, comment="Email único")
    password_hash = Column(String(255), nullable=False, comment="Hash de la contraseña")
    
    telefono = Column(String(20), nullable=True, comment="Teléfono de contacto")
    fecha_nacimiento = Column(Date, nullable=True, comment="Fecha de nacimiento")
    genero = Column(SQLEnum(GeneroEnum), nullable=True, comment="Género del usuario")
    
    foto_perfil_url = Column(String(500), nullable=True, comment="URL de la foto de perfil")
    direccion = Column(String(300), nullable=True, comment="Dirección del usuario")
    documento_identidad = Column(String(50), nullable=True, comment="Documento de identidad")
    
    activo = Column(Boolean, default=True, nullable=False, comment="Si el usuario está activo")
    
    # Relaciones
    gimnasio = relationship("Gimnasio", back_populates="usuarios")
    rol = relationship("Rol", back_populates="usuarios")
    
    # Relaciones como cliente
    membresias = relationship("Membresia", back_populates="usuario", cascade="all, delete-orphan", foreign_keys="Membresia.usuario_id")
    accesos = relationship("Acceso", back_populates="usuario", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")
    facturas = relationship("Factura", back_populates="usuario", cascade="all, delete-orphan")
    progreso_fisico = relationship("ProgresoFisico", back_populates="usuario", cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="usuario", cascade="all, delete-orphan")
    
    # Relaciones como entrenador
    clases_impartidas = relationship("Clase", back_populates="entrenador", foreign_keys="Clase.entrenador_id")
    clientes_asignados = relationship(
        "EntrenadorCliente",
        back_populates="entrenador",
        foreign_keys="EntrenadorCliente.entrenador_id",
        cascade="all, delete-orphan"
    )
    
    # Relación como cliente con entrenador
    entrenador_asignado = relationship(
        "EntrenadorCliente",
        back_populates="cliente",
        foreign_keys="EntrenadorCliente.cliente_id",
        cascade="all, delete-orphan"
    )
    
    # Rutinas creadas (como entrenador)
    rutinas_creadas = relationship(
        "Rutina",
        back_populates="creador",
        foreign_keys="Rutina.creador_id",
        cascade="all, delete-orphan"
    )
    
    # Rutinas asignadas (como cliente)
    rutinas_asignadas = relationship(
        "Rutina",
        back_populates="cliente",
        foreign_keys="Rutina.cliente_id",
        cascade="all, delete-orphan"
    )
    
    # Dietas (como entrenador y cliente)
    dietas_creadas = relationship(
        "Dieta",
        back_populates="entrenador",
        foreign_keys="Dieta.entrenador_id",
        cascade="all, delete-orphan"
    )
    dietas_asignadas = relationship(
        "Dieta",
        back_populates="cliente",
        foreign_keys="Dieta.cliente_id",
        cascade="all, delete-orphan"
    )
    
    # Logs de actividad
    logs_actividad = relationship("LogActividad", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}', nombre='{self.nombre_completo}')>"
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    @property
    def edad(self) -> int:
        """Calcula la edad del usuario basado en su fecha de nacimiento"""
        if not self.fecha_nacimiento:
            return None
        
        today = datetime.now().date()
        age = today.year - self.fecha_nacimiento.year
        
        # Ajustar si aún no ha cumplido años este año
        if today.month < self.fecha_nacimiento.month or \
           (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
            age -= 1
        
        return age
    
    def to_dict(self, include_sensitive=False):
        """
        Convierte el modelo a diccionario.
        
        Args:
            include_sensitive: Si incluir datos sensibles (password_hash)
        """
        data = {
            "id": self.id,
            "gimnasio_id": self.gimnasio_id,
            "rol_id": self.rol_id,
            "rol_nombre": self.rol.nombre if self.rol else None,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            "edad": self.edad,
            "genero": self.genero.value if self.genero else None,
            "foto_perfil_url": self.foto_perfil_url,
            "direccion": self.direccion,
            "documento_identidad": self.documento_identidad,
            "activo": self.activo,
            "fecha_creacion": self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            "fecha_actualizacion": self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
        }
        
        if include_sensitive:
            data["password_hash"] = self.password_hash
        
        return data
    
    def es_admin(self) -> bool:
        """Verifica si el usuario es admin o super_admin"""
        return self.rol and self.rol.nombre in ["super_admin", "admin"]
    
    def es_super_admin(self) -> bool:
        """Verifica si el usuario es super_admin"""
        return self.rol and self.rol.nombre == "super_admin"
    
    def es_entrenador(self) -> bool:
        """Verifica si el usuario es entrenador"""
        return self.rol and self.rol.nombre == "entrenador"
    
    def es_cliente(self) -> bool:
        """Verifica si el usuario es cliente"""
        return self.rol and self.rol.nombre == "cliente"