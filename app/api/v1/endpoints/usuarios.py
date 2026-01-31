"""Endpoints de Usuarios"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user, get_gimnasio_id
from app.services.usuario_service import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.utils.pagination import paginar, PaginationParams

router = APIRouter()

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crear nuevo usuario"""
    service = UsuarioService(db)
    return service.create(usuario)

@router.get("/", response_model=List[UsuarioResponse])
def get_usuarios(
    params: PaginationParams = Depends(),
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar usuarios del gimnasio"""
    service = UsuarioService(db)
    return service.get_all(gimnasio_id, skip=params.skip, limit=params.limit)

@router.get("/clientes", response_model=List[UsuarioResponse])
def get_clientes(
    params: PaginationParams = Depends(),
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar clientes del gimnasio"""
    service = UsuarioService(db)
    return service.get_clientes(gimnasio_id, skip=params.skip, limit=params.limit)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener usuario por ID"""
    service = UsuarioService(db)
    return service.get_by_id(usuario_id)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar usuario"""
    service = UsuarioService(db)
    return service.update(usuario_id, usuario)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar usuario"""
    service = UsuarioService(db)
    service.delete(usuario_id)