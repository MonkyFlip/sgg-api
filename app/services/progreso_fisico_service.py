"""Service de Progreso Físico"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.progreso_fisico import ProgresoFisicoRepository
from app.schemas.progreso_fisico import ProgresoFisicoCreate, ProgresoFisicoUpdate

class ProgresoFisicoService:
    def __init__(self, db: Session):
        self.repo = ProgresoFisicoRepository(db)
    
    def create(self, data: ProgresoFisicoCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
        return obj
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_usuario(usuario_id, skip, limit)
    
    def get_ultimo_registro(self, usuario_id: int):
        return self.repo.get_ultimo_registro(usuario_id)
    
    def update(self, id: int, data: ProgresoFisicoUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True