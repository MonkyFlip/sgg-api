"""Domain Interfaces"""
from app.domain.interfaces.repository_interface import IRepository
from app.domain.interfaces.usuario_repository_interface import IUsuarioRepository
from app.domain.interfaces.gimnasio_repository_interface import IGimnasioRepository

__all__ = [
    "IRepository",
    "IUsuarioRepository",
    "IGimnasioRepository",
]