"""Service de Horario de Clase"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.clase_horario import ClaseHorarioRepository
from app.schemas.clase_horario import ClaseHorarioCreate, ClaseHorarioUpdate

class ClaseHorarioService:
    def __init__(self, db: Session):
        self.repo = ClaseHorarioRepository(db)
    
    def create(self, data: ClaseHorarioCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Horario no encontrado")
        return obj
    
    def get_by_clase(self, clase_id: int):
        return self.repo.get_by_clase(clase_id)
    
    def update(self, id: int, data: ClaseHorarioUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True