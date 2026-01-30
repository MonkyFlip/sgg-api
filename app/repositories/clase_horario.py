"""Repository de Horario de Clase"""
from typing import List
from sqlalchemy.orm import Session
from app.models.clase_horario import ClaseHorario
from app.core.constants import DiaSemanaEnum
from app.repositories.base import BaseRepository

class ClaseHorarioRepository(BaseRepository[ClaseHorario]):
    def __init__(self, db: Session):
        super().__init__(ClaseHorario, db)
    
    def get_by_clase(self, clase_id: int) -> List[ClaseHorario]:
        """Obtiene horarios de una clase"""
        return self.db.query(ClaseHorario).filter(ClaseHorario.clase_id == clase_id).all()
    
    def get_by_dia(self, clase_id: int, dia_semana: DiaSemanaEnum) -> List[ClaseHorario]:
        """Obtiene horarios de una clase en un día específico"""
        return self.db.query(ClaseHorario).filter(
            ClaseHorario.clase_id == clase_id,
            ClaseHorario.dia_semana == dia_semana
        ).all()