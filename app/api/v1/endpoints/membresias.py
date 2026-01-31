"""Endpoints de Membresías"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user, get_gimnasio_id
from app.services.membresia_service import MembresiaService
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate, MembresiaResponse

router = APIRouter()

@router.post("/", response_model=MembresiaResponse, status_code=status.HTTP_201_CREATED)
def create_membresia(membresia: MembresiaCreate, db: Session = Depends(get_db)):
    """Crear nueva membresía"""
    service = MembresiaService(db)
    return service.create(membresia)

@router.get("/usuario/{usuario_id}", response_model=List[MembresiaResponse])
def get_membresias_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener membresías de un usuario"""
    service = MembresiaService(db)
    return service.get_by_usuario(usuario_id)

@router.get("/usuario/{usuario_id}/activa", response_model=MembresiaResponse)
def get_membresia_activa(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener membresía activa de un usuario"""
    service = MembresiaService(db)
    return service.get_activa_usuario(usuario_id)

@router.get("/{membresia_id}", response_model=MembresiaResponse)
def get_membresia(membresia_id: int, db: Session = Depends(get_db)):
    """Obtener membresía por ID"""
    service = MembresiaService(db)
    return service.get_by_id(membresia_id)

@router.put("/{membresia_id}", response_model=MembresiaResponse)
def update_membresia(
    membresia_id: int,
    membresia: MembresiaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar membresía"""
    service = MembresiaService(db)
    return service.update(membresia_id, membresia)

@router.post("/{membresia_id}/cancelar")
def cancelar_membresia(membresia_id: int, db: Session = Depends(get_db)):
    """Cancelar membresía"""
    service = MembresiaService(db)
    service.cancelar(membresia_id)
    return {"message": "Membresía cancelada"}