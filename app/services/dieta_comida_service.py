"""Service de Comida de Dieta"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.dieta_comida import DietaComidaRepository
from app.schemas.dieta_comida import DietaComidaCreate, DietaComidaUpdate

class DietaComidaService:
    def __init__(self, db: Session):
        self.repo = DietaComidaRepository(db)
    
    def create(self, data: DietaComidaCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comida no encontrada")
        return obj
    
    def get_by_dieta(self, dieta_id: int):
        return self.repo.get_by_dieta(dieta_id)
    
    def update(self, id: int, data: DietaComidaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True