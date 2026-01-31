"""Endpoints de Gimnasios"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, require_admin
from app.services.gimnasio_service import GimnasioService
from app.schemas.gimnasio import GimnasioCreate, GimnasioUpdate, GimnasioResponse

router = APIRouter()

@router.post("/", response_model=GimnasioResponse, status_code=status.HTTP_201_CREATED)
def create_gimnasio(
    gimnasio: GimnasioCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """Crear nuevo gimnasio"""
    service = GimnasioService(db)
    return service.create(gimnasio)

@router.get("/", response_model=List[GimnasioResponse])
def get_gimnasios(db: Session = Depends(get_db)):
    """Listar todos los gimnasios"""
    service = GimnasioService(db)
    return service.get_all()

@router.get("/{gimnasio_id}", response_model=GimnasioResponse)
def get_gimnasio(gimnasio_id: int, db: Session = Depends(get_db)):
    """Obtener gimnasio por ID"""
    service = GimnasioService(db)
    return service.get_by_id(gimnasio_id)

@router.put("/{gimnasio_id}", response_model=GimnasioResponse)
def update_gimnasio(
    gimnasio_id: int,
    gimnasio: GimnasioUpdate,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """Actualizar gimnasio"""
    service = GimnasioService(db)
    return service.update(gimnasio_id, gimnasio)

@router.delete("/{gimnasio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gimnasio(
    gimnasio_id: int,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    """Eliminar gimnasio"""
    service = GimnasioService(db)
    service.delete(gimnasio_id)