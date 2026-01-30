"""Repository de Producto"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.producto import Producto
from app.repositories.base import BaseRepository

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, db: Session):
        super().__init__(Producto, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, activo: bool = None, skip: int = 0, limit: int = 100) -> List[Producto]:
        """Obtiene productos de un gimnasio"""
        query = self.db.query(Producto).filter(Producto.gimnasio_id == gimnasio_id)
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        return query.offset(skip).limit(limit).all()
    
    def get_by_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtiene productos de una categoría"""
        return self.db.query(Producto).filter(Producto.categoria_id == categoria_id).all()
    
    def get_bajo_stock(self, gimnasio_id: int) -> List[Producto]:
        """Obtiene productos con stock bajo (stock_actual <= stock_minimo)"""
        return self.db.query(Producto).filter(
            and_(
                Producto.gimnasio_id == gimnasio_id,
                Producto.stock_actual <= Producto.stock_minimo
            )
        ).all()