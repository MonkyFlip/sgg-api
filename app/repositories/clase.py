"""Repository de Clase"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.clase import Clase
from app.repositories.base import BaseRepository

class ClaseRepository(BaseRepository[Clase]):
    def __init__(self, db: Session):
        super().__init__(Clase, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, activo: bool = None, skip: int = 0, limit: int = 100) -> List[Clase]:
        """Obtiene clases de un gimnasio"""
        query = self.db.query(Clase).filter(Clase.gimnasio_id == gimnasio_id)
        if activo is not None:
            query = query.filter(Clase.activo == activo)
        return query.offset(skip).limit(limit).all()
    
    def get_by_entrenador(self, entrenador_id: int, skip: int = 0, limit: int = 100) -> List[Clase]:
        """Obtiene clases de un entrenador"""
        return self.db.query(Clase).filter(Clase.entrenador_id == entrenador_id).offset(skip).limit(limit).all()