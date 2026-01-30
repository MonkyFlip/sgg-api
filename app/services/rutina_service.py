"""Service de Rutina"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.rutina import RutinaRepository
from app.schemas.rutina import RutinaCreate, RutinaUpdate

class RutinaService:
    def __init__(self, db: Session):
        self.repo = RutinaRepository(db)
    
    def create(self, data: RutinaCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rutina no encontrada")
        return obj
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_gimnasio(gimnasio_id, skip=skip, limit=limit)
    
    def get_by_cliente(self, cliente_id: int):
        return self.repo.get_by_cliente(cliente_id)
    
    def get_generales(self, gimnasio_id: int):
        return self.repo.get_generales(gimnasio_id)
    
    def update(self, id: int, data: RutinaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True