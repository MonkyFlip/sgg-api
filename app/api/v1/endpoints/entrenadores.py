"""Endpoints de Entrenadores"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_current_user, require_entrenador
from app.services.entrenador_service import EntrenadorService
from app.schemas.usuario import UsuarioResponse

router = APIRouter()

@router.get("/mis-clientes", response_model=List[UsuarioResponse])
def get_mis_clientes(
    current_user = Depends(require_entrenador),
    db: Session = Depends(get_db)
):
    """Obtener clientes asignados al entrenador"""
    service = EntrenadorService(db)
    return service.get_mis_clientes(current_user.id)

@router.post("/asignar-cliente")
def asignar_cliente(
    cliente_id: int,
    notas: str = None,
    current_user = Depends(require_entrenador),
    db: Session = Depends(get_db)
):
    """Asignar un cliente al entrenador"""
    service = EntrenadorService(db)
    service.asignar_cliente(current_user.id, cliente_id, notas)
    return {"message": "Cliente asignado exitosamente"}

@router.delete("/desasignar-cliente/{cliente_id}")
def desasignar_cliente(
    cliente_id: int,
    current_user = Depends(require_entrenador),
    db: Session = Depends(get_db)
):
    """Desasignar un cliente del entrenador"""
    service = EntrenadorService(db)
    service.desasignar_cliente(current_user.id, cliente_id)
    return {"message": "Cliente desasignado"}

@router.get("/estadisticas")
def get_estadisticas(
    current_user = Depends(require_entrenador),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas del entrenador"""
    service = EntrenadorService(db)
    return service.get_estadisticas(current_user.id)

@router.get("/clientes-sin-rutina", response_model=List[UsuarioResponse])
def get_clientes_sin_rutina(
    current_user = Depends(require_entrenador),
    db: Session = Depends(get_db)
):
    """Obtener clientes sin rutina asignada"""
    service = EntrenadorService(db)
    return service.get_clientes_sin_rutina(current_user.id)