"""Service de Acceso"""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.acceso import AccesoRepository
from app.repositories.usuario import UsuarioRepository
from app.repositories.membresia import MembresiaRepository
from app.schemas.acceso import RegistrarEntrada, RegistrarSalida
from app.core.constants import TipoAccesoEnum

class AccesoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AccesoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.membresia_repo = MembresiaRepository(db)
    
    def registrar_entrada(self, data: RegistrarEntrada, gimnasio_id: int):
        # Verificar usuario
        usuario = self.usuario_repo.get_by_id(data.usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Verificar que pertenezca al gimnasio
        if usuario.gimnasio_id != gimnasio_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no pertenece a este gimnasio")
        
        # Verificar membresía activa
        membresia_activa = self.membresia_repo.get_activa_usuario(data.usuario_id)
        if not membresia_activa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario no tiene una membresía activa"
            )
        
        # Verificar si ya tiene acceso abierto
        acceso_abierto = self.repo.get_acceso_abierto(data.usuario_id)
        if acceso_abierto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya tiene una entrada sin salida registrada"
            )
        
        # Registrar entrada
        acceso_data = {
            "usuario_id": data.usuario_id,
            "gimnasio_id": gimnasio_id,
            "fecha_hora_entrada": datetime.now(),
            "tipo_acceso": data.tipo_acceso
        }
        
        return self.repo.create(acceso_data)
    
    def registrar_salida(self, data: RegistrarSalida):
        # Buscar acceso abierto
        acceso = self.repo.get_acceso_abierto(data.usuario_id)
        if not acceso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró entrada sin salida para este usuario"
            )
        
        # Registrar salida
        return self.repo.update(acceso.id, {"fecha_hora_salida": datetime.now()})
    
    def get_usuarios_en_gimnasio(self, gimnasio_id: int):
        return self.repo.get_usuarios_en_gimnasio(gimnasio_id)
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_usuario(usuario_id, skip, limit)