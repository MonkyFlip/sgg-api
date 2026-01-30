"""Service de Producto"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.producto import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate

class ProductoService:
    def __init__(self, db: Session):
        self.repo = ProductoRepository(db)
    
    def create(self, data: ProductoCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return obj
    
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_gimnasio(gimnasio_id, skip=skip, limit=limit)
    
    def get_bajo_stock(self, gimnasio_id: int):
        return self.repo.get_bajo_stock(gimnasio_id)
    
    def update(self, id: int, data: ProductoUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True