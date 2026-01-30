"""Repository de Inventario"""
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.inventario import Inventario
from app.core.constants import EstadoEquipamientoEnum
from app.repositories.base import BaseRepository

class InventarioRepository(BaseRepository[Inventario]):
    def __init__(self, db: Session):
        super().__init__(Inventario, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, activo: bool = None, skip: int = 0, limit: int = 100) -> List[Inventario]:
        """Obtiene items de inventario de un gimnasio"""
        query = self.db.query(Inventario).filter(Inventario.gimnasio_id == gimnasio_id)
        if activo is not None:
            query = query.filter(Inventario.activo == activo)
        return query.offset(skip).limit(limit).all()
    
    def get_by_categoria(self, categoria_id: int) -> List[Inventario]:
        """Obtiene items por categoría"""
        return self.db.query(Inventario).filter(Inventario.categoria_id == categoria_id).all()
    
    def get_by_estado(self, gimnasio_id: int, estado: EstadoEquipamientoEnum) -> List[Inventario]:
        """Obtiene items por estado"""
        return self.db.query(Inventario).filter(
            and_(Inventario.gimnasio_id == gimnasio_id, Inventario.estado == estado)
        ).all()
    
    def get_requiere_mantenimiento(self, gimnasio_id: int) -> List[Inventario]:
        """Obtiene items que requieren mantenimiento próximamente"""
        return self.db.query(Inventario).filter(
            and_(
                Inventario.gimnasio_id == gimnasio_id,
                Inventario.fecha_proximo_mantenimiento.isnot(None),
                Inventario.fecha_proximo_mantenimiento <= date.today()
            )
        ).all()