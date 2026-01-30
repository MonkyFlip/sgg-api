"""Service de Pago"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.pago import PagoRepository
from app.repositories.factura import FacturaRepository
from app.schemas.pago import PagoCreate
from app.core.constants import EstadoFacturaEnum
from datetime import datetime

class PagoService:
    def __init__(self, db: Session):
        self.repo = PagoRepository(db)
        self.factura_repo = FacturaRepository(db)
    
    def create(self, data: PagoCreate):
        # Verificar factura
        factura = self.factura_repo.get_by_id(data.factura_id)
        if not factura:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
        
        pago = self.repo.create(data.model_dump())
        
        # Actualizar estado de factura si el pago cubre el total
        pagos = self.repo.get_by_factura(factura.id)
        total_pagado = sum(p.monto for p in pagos)
        
        if total_pagado >= factura.total:
            self.factura_repo.update(factura.id, {
                "estado": EstadoFacturaEnum.PAGADA,
                "fecha_pago": datetime.now()
            })
        
        return pago
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
        return obj
    
    def get_by_factura(self, factura_id: int):
        return self.repo.get_by_factura(factura_id)