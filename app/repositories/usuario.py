"""Repository de Usuario"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.usuario import Usuario
from app.repositories.base import BaseRepository

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: Session):
        super().__init__(Usuario, db)
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene usuario por email"""
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene usuarios de un gimnasio"""
        return self.db.query(Usuario).filter(Usuario.gimnasio_id == gimnasio_id).offset(skip).limit(limit).all()
    
    def get_by_rol(self, gimnasio_id: int, rol_nombre: str, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene usuarios por rol en un gimnasio"""
        return self.db.query(Usuario).join(Usuario.rol).filter(
            and_(Usuario.gimnasio_id == gimnasio_id, Usuario.rol.has(nombre=rol_nombre))
        ).offset(skip).limit(limit).all()
    
    def get_clientes(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene clientes de un gimnasio"""
        return self.get_by_rol(gimnasio_id, "cliente", skip, limit)
    
    def get_entrenadores(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene entrenadores de un gimnasio"""
        return self.get_by_rol(gimnasio_id, "entrenador", skip, limit)
    
    def get_activos(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtiene usuarios activos de un gimnasio"""
        return self.db.query(Usuario).filter(
            and_(Usuario.gimnasio_id == gimnasio_id, Usuario.activo == True)
        ).offset(skip).limit(limit).all()