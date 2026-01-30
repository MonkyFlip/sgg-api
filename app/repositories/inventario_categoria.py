"""Repository de Categoría de Inventario"""
from typing import List
from sqlalchemy.orm import Session
from app.models.inventario_categoria import InventarioCategoria
from app.repositories.base import BaseRepository

class InventarioCategoriaRepository(BaseRepository[InventarioCategoria]):
    def __init__(self, db: Session):
        super().__init__(InventarioCategoria, db)
    
    def get_by_gimnasio(self, gimnasio_id: int) -> List[InventarioCategoria]:
        """Obtiene categorías de inventario de un gimnasio"""
        return self.db.query(InventarioCategoria).filter(
            InventarioCategoria.gimnasio_id == gimnasio_id
        ).all()