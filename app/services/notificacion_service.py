"""Service de Notificación"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.notificacion import NotificacionRepository
from app.schemas.notificacion import NotificacionCreate, NotificacionUpdate
from datetime import datetime

class NotificacionService:
    def __init__(self, db: Session):
        self.repo = NotificacionRepository(db)
    
    def create(self, data: NotificacionCreate):
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notificación no encontrada")
        return obj
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_usuario(usuario_id, skip=skip, limit=limit)
    
    def get_no_leidas(self, usuario_id: int):
        return self.repo.get_no_leidas(usuario_id)
    
    def marcar_leida(self, id: int):
        return self.repo.update(id, {
            "leida": True,
            "fecha_lectura": datetime.now()
        })
    
    def marcar_todas_leidas(self, usuario_id: int):
        return self.repo.marcar_todas_leidas(usuario_id)
    
    def update(self, id: int, data: NotificacionUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True