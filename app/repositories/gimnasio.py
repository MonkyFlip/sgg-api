"""Repository de Gimnasio"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.gimnasio import Gimnasio
from app.repositories.base import BaseRepository

class GimnasioRepository(BaseRepository[Gimnasio]):
    def __init__(self, db: Session):
        super().__init__(Gimnasio, db)
    
    def get_by_codigo(self, codigo_unico: str) -> Optional[Gimnasio]:
        """Obtiene gimnasio por código único"""
        return self.db.query(Gimnasio).filter(Gimnasio.codigo_unico == codigo_unico).first()
    
    def get_by_email(self, email: str) -> Optional[Gimnasio]:
        """Obtiene gimnasio por email"""
        return self.db.query(Gimnasio).filter(Gimnasio.email == email).first()
    
    def get_activos(self, skip: int = 0, limit: int = 100):
        """Obtiene gimnasios activos"""
        return self.db.query(Gimnasio).filter(Gimnasio.activo == True).offset(skip).limit(limit).all()