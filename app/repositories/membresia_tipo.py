"""Repository de Tipo de Membresía"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.membresia_tipo import MembresiaTipo
from app.repositories.base import BaseRepository

class MembresiaTipoRepository(BaseRepository[MembresiaTipo]):
    def __init__(self, db: Session):
        super().__init__(MembresiaTipo, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[MembresiaTipo]:
        """Obtiene tipos de membresía de un gimnasio"""
        return self.db.query(MembresiaTipo).filter(
            MembresiaTipo.gimnasio_id == gimnasio_id
        ).offset(skip).limit(limit).all()
    
    def get_activos(self, gimnasio_id: int) -> List[MembresiaTipo]:
        """Obtiene tipos de membresía activos de un gimnasio"""
        return self.db.query(MembresiaTipo).filter(
            and_(MembresiaTipo.gimnasio_id == gimnasio_id, MembresiaTipo.activo == True)
        ).all()