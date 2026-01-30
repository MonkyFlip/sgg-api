"""Repository de Pago"""
from typing import List
from sqlalchemy.orm import Session
from app.models.pago import Pago
from app.repositories.base import BaseRepository

class PagoRepository(BaseRepository[Pago]):
    def __init__(self, db: Session):
        super().__init__(Pago, db)
    
    def get_by_factura(self, factura_id: int) -> List[Pago]:
        """Obtiene pagos de una factura"""
        return self.db.query(Pago).filter(Pago.factura_id == factura_id).all()