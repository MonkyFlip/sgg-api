"""Repository de Progreso Físico"""
from typing import List
from datetime import date
from sqlalchemy.orm import Session
from app.models.progreso_fisico import ProgresoFisico
from app.repositories.base import BaseRepository

class ProgresoFisicoRepository(BaseRepository[ProgresoFisico]):
    def __init__(self, db: Session):
        super().__init__(ProgresoFisico, db)
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[ProgresoFisico]:
        """Obtiene registros de progreso de un usuario"""
        return self.db.query(ProgresoFisico).filter(
            ProgresoFisico.usuario_id == usuario_id
        ).order_by(ProgresoFisico.fecha_registro.desc()).offset(skip).limit(limit).all()
    
    def get_ultimo_registro(self, usuario_id: int):
        """Obtiene el último registro de progreso de un usuario"""
        return self.db.query(ProgresoFisico).filter(
            ProgresoFisico.usuario_id == usuario_id
        ).order_by(ProgresoFisico.fecha_registro.desc()).first()
    
    def get_by_rango_fechas(self, usuario_id: int, fecha_inicio: date, fecha_fin: date) -> List[ProgresoFisico]:
        """Obtiene registros en un rango de fechas"""
        return self.db.query(ProgresoFisico).filter(
            ProgresoFisico.usuario_id == usuario_id,
            ProgresoFisico.fecha_registro >= fecha_inicio,
            ProgresoFisico.fecha_registro <= fecha_fin
        ).order_by(ProgresoFisico.fecha_registro).all()