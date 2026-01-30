"""Repository de Factura"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.factura import Factura
from app.core.constants import EstadoFacturaEnum
from app.repositories.base import BaseRepository

class FacturaRepository(BaseRepository[Factura]):
    def __init__(self, db: Session):
        super().__init__(Factura, db)
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List[Factura]:
        """Obtiene facturas de un gimnasio"""
        return self.db.query(Factura).filter(Factura.gimnasio_id == gimnasio_id).offset(skip).limit(limit).all()
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Factura]:
        """Obtiene facturas de un usuario"""
        return self.db.query(Factura).filter(Factura.usuario_id == usuario_id).offset(skip).limit(limit).all()
    
    def get_by_numero(self, numero_factura: str):
        """Obtiene factura por número"""
        return self.db.query(Factura).filter(Factura.numero_factura == numero_factura).first()
    
    def get_pendientes(self, gimnasio_id: int) -> List[Factura]:
        """Obtiene facturas pendientes de pago"""
        return self.db.query(Factura).filter(
            and_(
                Factura.gimnasio_id == gimnasio_id,
                Factura.estado == EstadoFacturaEnum.PENDIENTE
            )
        ).all()