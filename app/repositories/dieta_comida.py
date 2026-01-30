"""Repository de Comida de Dieta"""
from typing import List
from sqlalchemy.orm import Session
from app.models.dieta_comida import DietaComida
from app.repositories.base import BaseRepository

class DietaComidaRepository(BaseRepository[DietaComida]):
    def __init__(self, db: Session):
        super().__init__(DietaComida, db)
    
    def get_by_dieta(self, dieta_id: int) -> List[DietaComida]:
        """Obtiene comidas de una dieta"""
        return self.db.query(DietaComida).filter(
            DietaComida.dieta_id == dieta_id
        ).order_by(DietaComida.tipo_comida).all()