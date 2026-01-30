"""Repository de Acceso"""
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.acceso import Acceso
from app.repositories.base import BaseRepository

class AccesoRepository(BaseRepository[Acceso]):
    def __init__(self, db: Session):
        super().__init__(Acceso, db)
    
    def get_by_usuario(self, usuario_id: int, skip: int = 0, limit: int = 100) -> List[Acceso]:
        """Obtiene accesos de un usuario"""
        return self.db.query(Acceso).filter(
            Acceso.usuario_id == usuario_id
        ).order_by(Acceso.fecha_hora_entrada.desc()).offset(skip).limit(limit).all()
    
    def get_by_gimnasio(self, gimnasio_id: int, fecha: date = None, skip: int = 0, limit: int = 100) -> List[Acceso]:
        """Obtiene accesos de un gimnasio en una fecha específica"""
        query = self.db.query(Acceso).filter(Acceso.gimnasio_id == gimnasio_id)
        
        if fecha:
            inicio_dia = datetime.combine(fecha, datetime.min.time())
            fin_dia = datetime.combine(fecha, datetime.max.time())
            query = query.filter(
                and_(Acceso.fecha_hora_entrada >= inicio_dia, Acceso.fecha_hora_entrada <= fin_dia)
            )
        
        return query.order_by(Acceso.fecha_hora_entrada.desc()).offset(skip).limit(limit).all()
    
    def get_acceso_abierto(self, usuario_id: int) -> Optional[Acceso]:
        """Obtiene acceso abierto (sin salida) de un usuario"""
        return self.db.query(Acceso).filter(
            and_(Acceso.usuario_id == usuario_id, Acceso.fecha_hora_salida.is_(None))
        ).first()
    
    def get_usuarios_en_gimnasio(self, gimnasio_id: int) -> List[Acceso]:
        """Obtiene usuarios actualmente en el gimnasio (sin salida registrada)"""
        return self.db.query(Acceso).filter(
            and_(Acceso.gimnasio_id == gimnasio_id, Acceso.fecha_hora_salida.is_(None))
        ).all()
    
    def contar_visitas_usuario(self, usuario_id: int, fecha_inicio: date = None, fecha_fin: date = None) -> int:
        """Cuenta las visitas de un usuario en un rango de fechas"""
        query = self.db.query(Acceso).filter(Acceso.usuario_id == usuario_id)
        
        if fecha_inicio:
            query = query.filter(Acceso.fecha_hora_entrada >= datetime.combine(fecha_inicio, datetime.min.time()))
        if fecha_fin:
            query = query.filter(Acceso.fecha_hora_entrada <= datetime.combine(fecha_fin, datetime.max.time()))
        
        return query.count()