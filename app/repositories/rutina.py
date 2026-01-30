"""Repository de Rutina"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.rutina import Rutina
from app.repositories.base import BaseRepository

class RutinaRepository(BaseRepository[Rutina]):
    def __init__(self, db: Session):
        super().__init__(Rutina, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, activo: bool = None, skip: int = 0, limit: int = 100) -> List[Rutina]:
        """Obtiene rutinas de un gimnasio"""
        query = self.db.query(Rutina).filter(Rutina.gimnasio_id == gimnasio_id)
        if activo is not None:
            query = query.filter(Rutina.activo == activo)
        return query.offset(skip).limit(limit).all()
    
    def get_by_creador(self, creador_id: int) -> List[Rutina]:
        """Obtiene rutinas creadas por un entrenador"""
        return self.db.query(Rutina).filter(Rutina.creador_id == creador_id).all()
    
    def get_by_cliente(self, cliente_id: int) -> List[Rutina]:
        """Obtiene rutinas asignadas a un cliente"""
        return self.db.query(Rutina).filter(Rutina.cliente_id == cliente_id).all()
    
    def get_generales(self, gimnasio_id: int) -> List[Rutina]:
        """Obtiene rutinas generales (no asignadas a cliente específico)"""
        return self.db.query(Rutina).filter(
            and_(Rutina.gimnasio_id == gimnasio_id, Rutina.cliente_id.is_(None))
        ).all()