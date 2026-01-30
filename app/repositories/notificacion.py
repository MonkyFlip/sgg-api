"""Repository de Notificación"""
from typing import List
from sqlalchemy.orm import Session
from app.models.notificacion import Notificacion
from app.repositories.base import BaseRepository

class NotificacionRepository(BaseRepository[Notificacion]):
    def __init__(self, db: Session):
        super().__init__(Notificacion, db)
    
    def get_by_usuario(self, usuario_id: int, leida: bool = None, skip: int = 0, limit: int = 100) -> List[Notificacion]:
        """Obtiene notificaciones de un usuario"""
        query = self.db.query(Notificacion).filter(Notificacion.usuario_id == usuario_id)
        if leida is not None:
            query = query.filter(Notificacion.leida == leida)
        return query.order_by(Notificacion.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    def get_no_leidas(self, usuario_id: int) -> List[Notificacion]:
        """Obtiene notificaciones no leídas de un usuario"""
        return self.get_by_usuario(usuario_id, leida=False)
    
    def contar_no_leidas(self, usuario_id: int) -> int:
        """Cuenta notificaciones no leídas de un usuario"""
        return self.db.query(Notificacion).filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leida == False
        ).count()
    
    def marcar_todas_leidas(self, usuario_id: int) -> int:
        """Marca todas las notificaciones de un usuario como leídas"""
        from datetime import datetime
        count = self.db.query(Notificacion).filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leida == False
        ).update({
            "leida": True,
            "fecha_lectura": datetime.utcnow()
        })
        self.db.commit()
        return count