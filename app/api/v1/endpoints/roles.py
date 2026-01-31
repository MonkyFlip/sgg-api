"""Endpoints de Roles"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, require_admin
from app.services.rol_service import RolService
from app.schemas.rol import RolCreate, RolUpdate, RolResponse

router = APIRouter()

@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def create_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """Crear nuevo rol"""
    service = RolService(db)
    return service.create(rol)

@router.get("/", response_model=List[RolResponse])
def get_roles(db: Session = Depends(get_db)):
    """Listar todos los roles"""
    service = RolService(db)
    return service.get_all()

@router.get("/{rol_id}", response_model=RolResponse)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
    """Obtener rol por ID"""
    service = RolService(db)
    return service.get_by_id(rol_id)

@router.put("/{rol_id}", response_model=RolResponse)
def update_rol(
    rol_id: int,
    rol: RolUpdate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """Actualizar rol"""
    service = RolService(db)
    return service.update(rol_id, rol)