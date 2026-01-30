"""Repository de Reserva"""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reserva import Reserva
from app.core.constants import EstadoReservaEnum
from app.repositories.base import BaseRepository

class ReservaRepository(BaseRepository[Reserva]):
    def __init__(self, db: Session):
        super().__init__(Reserva, db)
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """Obtiene reservas de un usuario"""
        return self.db.query(Reserva).filter(Reserva.usuario_id == usuario_id).offset(skip).limit(limit).all()
    
    def get_by_horario_fecha(self, clase_horario_id: int, fecha_reserva: date) -> List[Reserva]:
        """Obtiene reservas de un horario en una fecha específica"""
        return self.db.query(Reserva).filter(
            and_(
                Reserva.clase_horario_id == clase_horario_id,
                Reserva.fecha_reserva == fecha_reserva,
                Reserva.estado == EstadoReservaEnum.CONFIRMADA
            )
        ).all()
    
    def contar_reservas_horario(self, clase_horario_id: int, fecha_reserva: date) -> int:
        """Cuenta reservas confirmadas de un horario en una fecha"""
        return self.db.query(Reserva).filter(
            and_(
                Reserva.clase_horario_id == clase_horario_id,
                Reserva.fecha_reserva == fecha_reserva,
                Reserva.estado == EstadoReservaEnum.CONFIRMADA
            )
        ).count()
    
    def tiene_reserva(self, usuario_id: int, clase_horario_id: int, fecha_reserva: date) -> bool:
        """Verifica si un usuario tiene reserva en un horario y fecha"""
        return self.db.query(Reserva).filter(
            and_(
                Reserva.usuario_id == usuario_id,
                Reserva.clase_horario_id == clase_horario_id,
                Reserva.fecha_reserva == fecha_reserva
            )
        ).count() > 0