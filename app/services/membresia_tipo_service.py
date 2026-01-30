"""Service de Tipo de Membresía"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.membresia_tipo import MembresiaTipoRepository
from app.schemas.membresia_tipo import MembresiaTipoCreate, MembresiaTipoUpdate

class MembresiaTipoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MembresiaTipoRepository(db)
    
    def create(self, data: MembresiaTipoCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        tipo = self.repo.get_by_id(id)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de membresía no encontrado")
        return tipo
    
    def get_by_gimnasio(self, gimnasio_id: int):
        return self.repo.get_by_gimnasio(gimnasio_id)
    
    def get_activos(self, gimnasio_id: int):
        return self.repo.get_activos(gimnasio_id)
    
    def update(self, id: int, data: MembresiaTipoUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo no encontrado")
        return True