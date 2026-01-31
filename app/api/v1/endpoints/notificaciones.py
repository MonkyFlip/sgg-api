"""Endpoints de Notificaciones"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user
from app.services.notificacion_service import NotificacionService
from app.schemas.notificacion import NotificacionCreate, NotificacionResponse

router = APIRouter()

@router.post("/", response_model=NotificacionResponse, status_code=status.HTTP_201_CREATED)
def create_notificacion(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    """Crear nueva notificación"""
    service = NotificacionService(db)
    return service.create(notificacion)

@router.get("/mis-notificaciones", response_model=List[NotificacionResponse])
def get_mis_notificaciones(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener notificaciones del usuario actual"""
    service = NotificacionService(db)
    return service.get_by_usuario(current_user.id)

@router.get("/no-leidas", response_model=List[NotificacionResponse])
def get_notificaciones_no_leidas(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener notificaciones no leídas"""
    service = NotificacionService(db)
    return service.get_no_leidas(current_user.id)

@router.post("/{notificacion_id}/marcar-leida")
def marcar_como_leida(
    notificacion_id: int,
    db: Session = Depends(get_db)
):
    """Marcar notificación como leída"""
    service = NotificacionService(db)
    service.marcar_leida(notificacion_id)
    return {"message": "Notificación marcada como leída"}

@router.post("/marcar-todas-leidas")
def marcar_todas_leidas(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marcar todas las notificaciones como leídas"""
    service = NotificacionService(db)
    service.marcar_todas_leidas(current_user.id)
    return {"message": "Todas las notificaciones marcadas como leídas"}