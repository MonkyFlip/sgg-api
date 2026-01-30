"""Repository de Entrenador-Cliente"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.entrenador_cliente import EntrenadorCliente
from app.repositories.base import BaseRepository

class EntrenadorClienteRepository(BaseRepository[EntrenadorCliente]):
    def __init__(self, db: Session):
        super().__init__(EntrenadorCliente, db)
    
    def get_clientes_entrenador(self, entrenador_id: int, activo: bool = True) -> List[EntrenadorCliente]:
        """Obtiene clientes asignados a un entrenador"""
        query = self.db.query(EntrenadorCliente).filter(EntrenadorCliente.entrenador_id == entrenador_id)
        if activo:
            query = query.filter(EntrenadorCliente.activo == True)
        return query.all()
    
    def get_entrenador_cliente(self, cliente_id: int) -> Optional[EntrenadorCliente]:
        """Obtiene el entrenador asignado a un cliente"""
        return self.db.query(EntrenadorCliente).filter(
            and_(EntrenadorCliente.cliente_id == cliente_id, EntrenadorCliente.activo == True)
        ).first()
    
    def existe_relacion(self, entrenador_id: int, cliente_id: int) -> bool:
        """Verifica si existe una relación activa entre entrenador y cliente"""
        return self.db.query(EntrenadorCliente).filter(
            and_(
                EntrenadorCliente.entrenador_id == entrenador_id,
                EntrenadorCliente.cliente_id == cliente_id,
                EntrenadorCliente.activo == True
            )
        ).count() > 0