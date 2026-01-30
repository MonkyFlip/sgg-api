"""Repository de Membresía"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.membresia import Membresia
from app.core.constants import EstadoMembresiaEnum
from app.repositories.base import BaseRepository

class MembresiaRepository(BaseRepository[Membresia]):
    def __init__(self, db: Session):
        super().__init__(Membresia, db)
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Membresia]:
        """Obtiene membresías de un usuario"""
        return self.db.query(Membresia).filter(
            Membresia.usuario_id == usuario_id
        ).offset(skip).limit(limit).all()
    
    def get_activa_usuario(self, usuario_id: int) -> Optional[Membresia]:
        """Obtiene membresía activa actual de un usuario"""
        return self.db.query(Membresia).filter(
            and_(
                Membresia.usuario_id == usuario_id,
                Membresia.estado == EstadoMembresiaEnum.ACTIVA,
                Membresia.fecha_inicio <= date.today(),
                Membresia.fecha_fin >= date.today()
            )
        ).first()
    
    def get_proximas_vencer(self, dias: int = 7) -> List[Membresia]:
        """Obtiene membresías que vencen en los próximos N días"""
        fecha_limite = date.today() + timedelta(days=dias)
        return self.db.query(Membresia).filter(
            and_(
                Membresia.estado == EstadoMembresiaEnum.ACTIVA,
                Membresia.fecha_fin <= fecha_limite,
                Membresia.fecha_fin >= date.today()
            )
        ).all()
    
    def get_vencidas(self) -> List[Membresia]:
        """Obtiene membresías vencidas que aún están marcadas como activas"""
        return self.db.query(Membresia).filter(
            and_(
                Membresia.estado == EstadoMembresiaEnum.ACTIVA,
                Membresia.fecha_fin < date.today()
            )
        ).all()

from datetime import timedelta