"""Service de Inventario"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.inventario import InventarioRepository
from app.schemas.inventario import InventarioCreate, InventarioUpdate

class InventarioService:
    def __init__(self, db: Session):
        self.repo = InventarioRepository(db)
    
    def create(self, data: InventarioCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
        return obj
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_gimnasio(gimnasio_id, skip=skip, limit=limit)
    
    def get_requiere_mantenimiento(self, gimnasio_id: int):
        return self.repo.get_requiere_mantenimiento(gimnasio_id)
    
    def update(self, id: int, data: InventarioUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True