"""Service de Factura"""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.factura import FacturaRepository
from app.schemas.factura import FacturaCreate
from app.core.constants import EstadoFacturaEnum
import random

class FacturaService:
    def __init__(self, db: Session):
        self.repo = FacturaRepository(db)
    
    def create(self, data: FacturaCreate):
        # Generar número de factura único
        numero_factura = self._generar_numero_factura()
        
        # Calcular totales
        subtotal = sum(d.precio_unitario * d.cantidad for d in data.detalles)
        total = subtotal + (data.impuestos if hasattr(data, 'impuestos') else 0) - (data.descuentos if hasattr(data, 'descuentos') else 0)
        
        factura_data = {
            "gimnasio_id": data.gimnasio_id,
            "usuario_id": data.usuario_id,
            "numero_factura": numero_factura,
            "tipo": data.tipo,
            "subtotal": subtotal,
            "impuestos": getattr(data, 'impuestos', 0),
            "descuentos": getattr(data, 'descuentos', 0),
            "total": total,
            "estado": EstadoFacturaEnum.PENDIENTE,
            "metodo_pago": data.metodo_pago,
            "notas": data.notas,
            "fecha_emision": datetime.now()
        }
        
        factura = self.repo.create(factura_data)
        
        # Crear detalles
        # (esto requeriría acceso a FacturaDetalleRepository)
        
        return factura
    
    def _generar_numero_factura(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"FAC-{timestamp}-{random_num}"
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada")
        return obj
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_gimnasio(gimnasio_id, skip, limit)
    
    def get_by_usuario(self, usuario_id: int):
        return self.repo.get_by_usuario(usuario_id)