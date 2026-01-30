"""Service de Dieta"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.dieta import DietaRepository
from app.schemas.dieta import DietaCreate, DietaUpdate

class DietaService:
    def __init__(self, db: Session):
        self.repo = DietaRepository(db)
    
    def create(self, data: DietaCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dieta no encontrada")
        return obj
    
    def get_by_cliente(self, cliente_id: int):
        return self.repo.get_by_cliente(cliente_id)
    
    def get_activa_cliente(self, cliente_id: int):
        return self.repo.get_activa_cliente(cliente_id)
    
    def update(self, id: int, data: DietaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True