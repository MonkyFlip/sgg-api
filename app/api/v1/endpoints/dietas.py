"""Endpoints de Dietas"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.services.dieta_service import DietaService
from app.schemas.dieta import DietaCreate, DietaUpdate, DietaResponse

router = APIRouter()

@router.post("/", response_model=DietaResponse, status_code=status.HTTP_201_CREATED)
def create_dieta(dieta: DietaCreate, db: Session = Depends(get_db)):
    """Crear nueva dieta"""
    service = DietaService(db)
    return service.create(dieta)

@router.get("/cliente/{cliente_id}", response_model=List[DietaResponse])
def get_dietas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener dietas de un cliente"""
    service = DietaService(db)
    return service.get_by_cliente(cliente_id)

@router.get("/cliente/{cliente_id}/activa", response_model=DietaResponse)
def get_dieta_activa(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener dieta activa de un cliente"""
    service = DietaService(db)
    return service.get_activa_cliente(cliente_id)

@router.get("/{dieta_id}", response_model=DietaResponse)
def get_dieta(dieta_id: int, db: Session = Depends(get_db)):
    """Obtener dieta por ID"""
    service = DietaService(db)
    return service.get_by_id(dieta_id)

@router.put("/{dieta_id}", response_model=DietaResponse)
def update_dieta(
    dieta_id: int,
    dieta: DietaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar dieta"""
    service = DietaService(db)
    return service.update(dieta_id, dieta)

@router.delete("/{dieta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dieta(dieta_id: int, db: Session = Depends(get_db)):
    """Eliminar dieta"""
    service = DietaService(db)
    service.delete(dieta_id)