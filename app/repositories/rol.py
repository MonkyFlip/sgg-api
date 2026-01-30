"""Repository de Rol"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.repositories.base import BaseRepository

class RolRepository(BaseRepository[Rol]):
    def __init__(self, db: Session):
        super().__init__(Rol, db)
    
    def get_by_nombre(self, nombre: str) -> Optional[Rol]:
        """Obtiene rol por nombre"""
        return self.db.query(Rol).filter(Rol.nombre == nombre).first()