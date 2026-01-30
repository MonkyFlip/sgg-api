"""Repository de Dieta"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.dieta import Dieta
from app.repositories.base import BaseRepository

class DietaRepository(BaseRepository[Dieta]):
    def __init__(self, db: Session):
        super().__init__(Dieta, db)
    
    def get_by_entrenador(self, entrenador_id: int) -> List[Dieta]:
        """Obtiene dietas creadas por un entrenador"""
        return self.db.query(Dieta).filter(Dieta.entrenador_id == entrenador_id).all()
    
    def get_by_cliente(self, cliente_id: int) -> List[Dieta]:
        """Obtiene dietas de un cliente"""
        return self.db.query(Dieta).filter(Dieta.cliente_id == cliente_id).all()
    
    def get_activa_cliente(self, cliente_id: int) -> Optional[Dieta]:
        """Obtiene dieta activa actual de un cliente"""
        return self.db.query(Dieta).filter(
            and_(
                Dieta.cliente_id == cliente_id,
                Dieta.activo == True,
                Dieta.fecha_inicio <= date.today(),
                or_(Dieta.fecha_fin.is_(None), Dieta.fecha_fin >= date.today())
            )
        ).first()

from sqlalchemy import or_