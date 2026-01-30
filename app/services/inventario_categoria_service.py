"""Service de Categoría de Inventario"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.inventario_categoria import InventarioCategoriaRepository
from app.schemas.inventario_categoria import InventarioCategoriaCreate, InventarioCategoriaUpdate

class InventarioCategoriaService:
    def __init__(self, db: Session):
        self.repo = InventarioCategoriaRepository(db)
    
    def create(self, data: InventarioCategoriaCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
        return obj
    
    def get_by_gimnasio(self, gimnasio_id: int):
        return self.repo.get_by_gimnasio(gimnasio_id)
    
    def update(self, id: int, data: InventarioCategoriaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True