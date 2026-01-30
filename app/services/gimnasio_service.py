"""Service de Gimnasio"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.gimnasio import GimnasioRepository
from app.schemas.gimnasio import GimnasioCreate, GimnasioUpdate

class GimnasioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = GimnasioRepository(db)
    
    def create(self, data: GimnasioCreate):
        # Verificar que el código único no exista
        if self.repo.get_by_codigo(data.codigo_unico):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de gimnasio ya existe"
            )
        
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        gimnasio = self.repo.get_by_id(id)
        if not gimnasio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gimnasio no encontrado"
            )
        return gimnasio
    
    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip=skip, limit=limit)
    
    def update(self, id: int, data: GimnasioUpdate):
        gimnasio = self.get_by_id(id)
        
        update_data = data.model_dump(exclude_unset=True)
        
        # Verificar email si se está actualizando
        if "email" in update_data:
            existing = self.repo.get_by_email(update_data["email"])
            if existing and existing.id != id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso"
                )
        
        return self.repo.update(id, update_data)
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gimnasio no encontrado"
            )
        return True