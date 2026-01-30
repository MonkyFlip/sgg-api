"""Service de Membresía"""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.membresia import MembresiaRepository
from app.repositories.usuario import UsuarioRepository
from app.repositories.membresia_tipo import MembresiaTipoRepository
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate
from app.core.constants import EstadoMembresiaEnum

class MembresiaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MembresiaRepository(db)
        self.usuario_repo = UsuarioRepository(db)
        self.tipo_repo = MembresiaTipoRepository(db)
    
    def create(self, data: MembresiaCreate):
        # Verificar usuario
        if not self.usuario_repo.exists(data.usuario_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Verificar tipo de membresía
        tipo = self.tipo_repo.get_by_id(data.membresia_tipo_id)
        if not tipo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de membresía no encontrado")
        
        # Verificar si ya tiene membresía activa
        membresia_activa = self.repo.get_activa_usuario(data.usuario_id)
        if membresia_activa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El usuario ya tiene una membresía activa que vence el {membresia_activa.fecha_fin}"
            )
        
        # Calcular fecha_fin si no se proporciona
        membresia_data = data.model_dump()
        if not membresia_data.get("fecha_fin"):
            membresia_data["fecha_fin"] = data.fecha_inicio + timedelta(days=tipo.duracion_dias)
        
        membresia_data["estado"] = EstadoMembresiaEnum.ACTIVA
        
        return self.repo.create(membresia_data)
    
    def get_by_id(self, id: int):
        membresia = self.repo.get_by_id(id)
        if not membresia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membresía no encontrada")
        return membresia
    
    def get_by_usuario(self, usuario_id: int):
        return self.repo.get_by_usuario(usuario_id)
    
    def get_activa_usuario(self, usuario_id: int):
        return self.repo.get_activa_usuario(usuario_id)
    
    def update(self, id: int, data: MembresiaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def cancelar(self, id: int):
        membresia = self.get_by_id(id)
        return self.repo.update(id, {"estado": EstadoMembresiaEnum.CANCELADA})
    
    def actualizar_vencidas(self):
        """Actualiza el estado de membresías vencidas"""
        vencidas = self.repo.get_vencidas()
        count = 0
        for membresia in vencidas:
            self.repo.update(membresia.id, {"estado": EstadoMembresiaEnum.VENCIDA})
            count += 1
        return count