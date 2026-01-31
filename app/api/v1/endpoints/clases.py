"""Endpoints de Clases"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id
from app.services.clase_service import ClaseService
from app.schemas.clase import ClaseCreate, ClaseUpdate, ClaseResponse

router = APIRouter()

@router.post("/", response_model=ClaseResponse, status_code=status.HTTP_201_CREATED)
def create_clase(clase: ClaseCreate, db: Session = Depends(get_db)):
    """Crear nueva clase grupal"""
    service = ClaseService(db)
    return service.create(clase)

@router.get("/", response_model=List[ClaseResponse])
def get_clases(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar clases del gimnasio"""
    service = ClaseService(db)
    return service.get_by_gimnasio(gimnasio_id)

@router.get("/{clase_id}", response_model=ClaseResponse)
def get_clase(clase_id: int, db: Session = Depends(get_db)):
    """Obtener clase por ID"""
    service = ClaseService(db)
    return service.get_by_id(clase_id)

@router.put("/{clase_id}", response_model=ClaseResponse)
def update_clase(
    clase_id: int,
    clase: ClaseUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar clase"""
    service = ClaseService(db)
    return service.update(clase_id, clase)

@router.delete("/{clase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clase(clase_id: int, db: Session = Depends(get_db)):
    """Eliminar clase"""
    service = ClaseService(db)
    service.delete(clase_id)