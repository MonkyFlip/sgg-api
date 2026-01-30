"""Repository de Ejercicio de Rutina"""
from typing import List
from sqlalchemy.orm import Session
from app.models.rutina_ejercicio import RutinaEjercicio
from app.core.constants import DiaSemanaEnum
from app.repositories.base import BaseRepository

class RutinaEjercicioRepository(BaseRepository[RutinaEjercicio]):
    def __init__(self, db: Session):
        super().__init__(RutinaEjercicio, db)
    
    def get_by_rutina(self, rutina_id: int) -> List[RutinaEjercicio]:
        """Obtiene ejercicios de una rutina"""
        return self.db.query(RutinaEjercicio).filter(
            RutinaEjercicio.rutina_id == rutina_id
        ).order_by(RutinaEjercicio.dia_semana, RutinaEjercicio.orden).all()
    
    def get_by_dia(self, rutina_id: int, dia_semana: DiaSemanaEnum) -> List[RutinaEjercicio]:
        """Obtiene ejercicios de un día específico"""
        return self.db.query(RutinaEjercicio).filter(
            RutinaEjercicio.rutina_id == rutina_id,
            RutinaEjercicio.dia_semana == dia_semana
        ).order_by(RutinaEjercicio.orden).all()