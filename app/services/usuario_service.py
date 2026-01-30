"""Service de Usuario"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.usuario import UsuarioRepository
from app.repositories.gimnasio import GimnasioRepository
from app.repositories.rol import RolRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, validate_password_strength

class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsuarioRepository(db)
        self.gimnasio_repo = GimnasioRepository(db)
        self.rol_repo = RolRepository(db)
    
    def create(self, data: UsuarioCreate):
        # Verificar email único
        if self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Verificar gimnasio
        if not self.gimnasio_repo.exists(data.gimnasio_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gimnasio no encontrado"
            )
        
        # Verificar rol
        if not self.rol_repo.exists(data.rol_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Validar contraseña
        if not validate_password_strength(data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña no cumple los requisitos de seguridad"
            )
        
        usuario_data = data.model_dump(exclude={"password"})
        usuario_data["password_hash"] = get_password_hash(data.password)
        
        return self.repo.create(usuario_data)
    
    def get_by_id(self, id: int):
        usuario = self.repo.get_by_id(id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return usuario
    
    def get_all(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_gimnasio(gimnasio_id, skip, limit)
    
    def get_clientes(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_clientes(gimnasio_id, skip, limit)
    
    def get_entrenadores(self, gimnasio_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_entrenadores(gimnasio_id, skip, limit)
    
    def update(self, id: int, data: UsuarioUpdate):
        usuario = self.get_by_id(id)
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, update_data)
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return True