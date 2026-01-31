"""Endpoints de Rutinas"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id, require_entrenador
from app.services.rutina_service import RutinaService
from app.schemas.rutina import RutinaCreate, RutinaUpdate, RutinaResponse

router = APIRouter()

@router.post("/", response_model=RutinaResponse, status_code=status.HTTP_201_CREATED)
def create_rutina(rutina: RutinaCreate, db: Session = Depends(get_db)):
    """Crear nueva rutina de entrenamiento"""
    service = RutinaService(db)
    return service.create(rutina)

@router.get("/", response_model=List[RutinaResponse])
def get_rutinas(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar rutinas del gimnasio"""
    service = RutinaService(db)
    return service.get_by_gimnasio(gimnasio_id)

@router.get("/generales", response_model=List[RutinaResponse])
def get_rutinas_generales(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar rutinas generales (no personalizadas)"""
    service = RutinaService(db)
    return service.get_generales(gimnasio_id)

@router.get("/cliente/{cliente_id}", response_model=List[RutinaResponse])
def get_rutinas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener rutinas de un cliente"""
    service = RutinaService(db)
    return service.get_by_cliente(cliente_id)

@router.get("/{rutina_id}", response_model=RutinaResponse)
def get_rutina(rutina_id: int, db: Session = Depends(get_db)):
    """Obtener rutina por ID"""
    service = RutinaService(db)
    return service.get_by_id(rutina_id)

@router.put("/{rutina_id}", response_model=RutinaResponse)
def update_rutina(
    rutina_id: int,
    rutina: RutinaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar rutina"""
    service = RutinaService(db)
    return service.update(rutina_id, rutina)

@router.delete("/{rutina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rutina(rutina_id: int, db: Session = Depends(get_db)):
    """Eliminar rutina"""
    service = RutinaService(db)
    service.delete(rutina_id)