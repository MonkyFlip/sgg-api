"""
Schemas module - Schemas Pydantic para validación de datos
"""

from app.schemas.base import ResponseBase, PaginatedResponse
from app.schemas.auth import Token, TokenData, Login, Register, PasswordChange, PasswordReset
from app.schemas.gimnasio import GimnasioCreate, GimnasioUpdate, GimnasioResponse
from app.schemas.rol import RolCreate, RolUpdate, RolResponse
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioDetail
from app.schemas.membresia_tipo import MembresiaTipoCreate, MembresiaTipoUpdate, MembresiaTipoResponse
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate, MembresiaResponse
from app.schemas.acceso import AccesoCreate, AccesoResponse, RegistrarEntrada, RegistrarSalida
from app.schemas.entrenador_cliente import EntrenadorClienteCreate, EntrenadorClienteUpdate, EntrenadorClienteResponse
from app.schemas.clase import ClaseCreate, ClaseUpdate, ClaseResponse
from app.schemas.clase_horario import ClaseHorarioCreate, ClaseHorarioUpdate, ClaseHorarioResponse
from app.schemas.reserva import ReservaCreate, ReservaUpdate, ReservaResponse
from app.schemas.producto_categoria import ProductoCategoriaCreate, ProductoCategoriaUpdate, ProductoCategoriaResponse
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.schemas.factura import FacturaCreate, FacturaResponse, FacturaDetalleCreate
from app.schemas.pago import PagoCreate, PagoResponse
from app.schemas.inventario_categoria import InventarioCategoriaCreate, InventarioCategoriaUpdate, InventarioCategoriaResponse
from app.schemas.inventario import InventarioCreate, InventarioUpdate, InventarioResponse
from app.schemas.rutina import RutinaCreate, RutinaUpdate, RutinaResponse
from app.schemas.rutina_ejercicio import RutinaEjercicioCreate, RutinaEjercicioUpdate, RutinaEjercicioResponse
from app.schemas.dieta import DietaCreate, DietaUpdate, DietaResponse
from app.schemas.dieta_comida import DietaComidaCreate, DietaComidaUpdate, DietaComidaResponse
from app.schemas.progreso_fisico import ProgresoFisicoCreate, ProgresoFisicoUpdate, ProgresoFisicoResponse
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate, NotificacionResponse
from app.schemas.pagination import PaginationParams

__all__ = [
    # Base
    "ResponseBase", "PaginatedResponse",
    # Auth
    "Token", "TokenData", "Login", "Register", "PasswordChange", "PasswordReset",
    # Gimnasio
    "GimnasioCreate", "GimnasioUpdate", "GimnasioResponse",
    # Rol
    "RolCreate", "RolUpdate", "RolResponse",
    # Usuario
    "UsuarioCreate", "UsuarioUpdate", "UsuarioResponse", "UsuarioDetail",
    # Membresia
    "MembresiaTipoCreate", "MembresiaTipoUpdate", "MembresiaTipoResponse",
    "MembresiaCreate", "MembresiaUpdate", "MembresiaResponse",
    # Acceso
    "AccesoCreate", "AccesoResponse", "RegistrarEntrada", "RegistrarSalida",
    # Entrenador-Cliente
    "EntrenadorClienteCreate", "EntrenadorClienteUpdate", "EntrenadorClienteResponse",
    # Clases
    "ClaseCreate", "ClaseUpdate", "ClaseResponse",
    "ClaseHorarioCreate", "ClaseHorarioUpdate", "ClaseHorarioResponse",
    "ReservaCreate", "ReservaUpdate", "ReservaResponse",
    # Productos
    "ProductoCategoriaCreate", "ProductoCategoriaUpdate", "ProductoCategoriaResponse",
    "ProductoCreate", "ProductoUpdate", "ProductoResponse",
    # Facturación
    "FacturaCreate", "FacturaResponse", "FacturaDetalleCreate",
    "PagoCreate", "PagoResponse",
    # Inventario
    "InventarioCategoriaCreate", "InventarioCategoriaUpdate", "InventarioCategoriaResponse",
    "InventarioCreate", "InventarioUpdate", "InventarioResponse",
    # Rutinas
    "RutinaCreate", "RutinaUpdate", "RutinaResponse",
    "RutinaEjercicioCreate", "RutinaEjercicioUpdate", "RutinaEjercicioResponse",
    # Dietas
    "DietaCreate", "DietaUpdate", "DietaResponse",
    "DietaComidaCreate", "DietaComidaUpdate", "DietaComidaResponse",
    # Progreso
    "ProgresoFisicoCreate", "ProgresoFisicoUpdate", "ProgresoFisicoResponse",
    # Notificaciones
    "NotificacionCreate", "NotificacionUpdate", "NotificacionResponse",
    # Pagination
    "PaginationParams",
]