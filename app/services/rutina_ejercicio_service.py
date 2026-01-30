"""Service de Ejercicio de Rutina"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.rutina_ejercicio import RutinaEjercicioRepository
from app.schemas.rutina_ejercicio import RutinaEjercicioCreate, RutinaEjercicioUpdate

class RutinaEjercicioService:
    def __init__(self, db: Session):
        self.repo = RutinaEjercicioRepository(db)
    
    def create(self, data: RutinaEjercicioCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ejercicio no encontrado")
        return obj
    
    def get_by_rutina(self, rutina_id: int):
        return self.repo.get_by_rutina(rutina_id)
    
    def update(self, id: int, data: RutinaEjercicioUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True