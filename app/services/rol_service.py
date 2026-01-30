"""Service de Rol"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.rol import RolRepository
from app.schemas.rol import RolCreate, RolUpdate

class RolService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RolRepository(db)
    
    def create(self, data: RolCreate):
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El rol ya existe"
            )
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        rol = self.repo.get_by_id(id)
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
        return rol
    
    def get_all(self):
        return self.repo.get_all()
    
    def update(self, id: int, data: RolUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, update_data)