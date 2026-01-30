"""
Repositories module - Repositorios para acceso a datos
"""

from app.repositories.base import BaseRepository
from app.repositories.gimnasio import GimnasioRepository
from app.repositories.rol import RolRepository
from app.repositories.usuario import UsuarioRepository
from app.repositories.membresia_tipo import MembresiaTipoRepository
from app.repositories.membresia import MembresiaRepository
from app.repositories.acceso import AccesoRepository
from app.repositories.entrenador_cliente import EntrenadorClienteRepository
from app.repositories.clase import ClaseRepository
from app.repositories.clase_horario import ClaseHorarioRepository
from app.repositories.reserva import ReservaRepository
from app.repositories.producto_categoria import ProductoCategoriaRepository
from app.repositories.producto import ProductoRepository
from app.repositories.factura import FacturaRepository
from app.repositories.pago import PagoRepository
from app.repositories.inventario_categoria import InventarioCategoriaRepository
from app.repositories.inventario import InventarioRepository
from app.repositories.rutina import RutinaRepository
from app.repositories.rutina_ejercicio import RutinaEjercicioRepository
from app.repositories.dieta import DietaRepository
from app.repositories.dieta_comida import DietaComidaRepository
from app.repositories.progreso_fisico import ProgresoFisicoRepository
from app.repositories.notificacion import NotificacionRepository

__all__ = [
    "BaseRepository",
    "GimnasioRepository",
    "RolRepository",
    "UsuarioRepository",
    "MembresiaTipoRepository",
    "MembresiaRepository",
    "AccesoRepository",
    "EntrenadorClienteRepository",
    "ClaseRepository",
    "ClaseHorarioRepository",
    "ReservaRepository",
    "ProductoCategoriaRepository",
    "ProductoRepository",
    "FacturaRepository",
    "PagoRepository",
    "InventarioCategoriaRepository",
    "InventarioRepository",
    "RutinaRepository",
    "RutinaEjercicioRepository",
    "DietaRepository",
    "DietaComidaRepository",
    "ProgresoFisicoRepository",
    "NotificacionRepository",
]