"""Endpoints de Reservas"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.services.reserva_service import ReservaService
from app.schemas.reserva import ReservaCreate, ReservaUpdate, ReservaResponse

router = APIRouter()

@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Crear nueva reserva de clase"""
    service = ReservaService(db)
    return service.create(reserva)

@router.get("/usuario/{usuario_id}", response_model=List[ReservaResponse])
def get_reservas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener reservas de un usuario"""
    service = ReservaService(db)
    return service.get_by_usuario(usuario_id)

@router.get("/{reserva_id}", response_model=ReservaResponse)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener reserva por ID"""
    service = ReservaService(db)
    return service.get_by_id(reserva_id)

@router.put("/{reserva_id}", response_model=ReservaResponse)
def update_reserva(
    reserva_id: int,
    reserva: ReservaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar reserva"""
    service = ReservaService(db)
    return service.update(reserva_id, reserva)

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Cancelar reserva"""
    service = ReservaService(db)
    service.delete(reserva_id)