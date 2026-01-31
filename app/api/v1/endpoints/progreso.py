"""Endpoints de Progreso Físico"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.services.progreso_fisico_service import ProgresoFisicoService
from app.services.progreso_service import ProgresoService
from app.schemas.progreso_fisico import ProgresoFisicoCreate, ProgresoFisicoUpdate, ProgresoFisicoResponse

router = APIRouter()

@router.post("/", response_model=ProgresoFisicoResponse, status_code=status.HTTP_201_CREATED)
def create_progreso(progreso: ProgresoFisicoCreate, db: Session = Depends(get_db)):
    """Registrar nuevo progreso físico"""
    service = ProgresoFisicoService(db)
    return service.create(progreso)

@router.get("/usuario/{usuario_id}", response_model=List[ProgresoFisicoResponse])
def get_progreso_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener progreso físico de un usuario"""
    service = ProgresoFisicoService(db)
    return service.get_by_usuario(usuario_id)

@router.get("/usuario/{usuario_id}/ultimo", response_model=ProgresoFisicoResponse)
def get_ultimo_progreso(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener último registro de progreso"""
    service = ProgresoFisicoService(db)
    return service.get_ultimo_registro(usuario_id)

@router.get("/usuario/{usuario_id}/analisis")
def get_analisis_progreso(usuario_id: int, dias: int = 30, db: Session = Depends(get_db)):
    """Obtener análisis de progreso"""
    service = ProgresoService(db)
    return service.calcular_progreso(usuario_id, dias)

@router.get("/usuario/{usuario_id}/objetivos")
def get_objetivos(
    usuario_id: int,
    peso_objetivo: float = None,
    grasa_objetivo: float = None,
    musculo_objetivo: float = None,
    db: Session = Depends(get_db)
):
    """Calcular progreso hacia objetivos"""
    service = ProgresoService(db)
    return service.calcular_objetivos(usuario_id, peso_objetivo, grasa_objetivo, musculo_objetivo)

@router.get("/{progreso_id}", response_model=ProgresoFisicoResponse)
def get_progreso(progreso_id: int, db: Session = Depends(get_db)):
    """Obtener progreso por ID"""
    service = ProgresoFisicoService(db)
    return service.get_by_id(progreso_id)

@router.put("/{progreso_id}", response_model=ProgresoFisicoResponse)
def update_progreso(
    progreso_id: int,
    progreso: ProgresoFisicoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar progreso"""
    service = ProgresoFisicoService(db)
    return service.update(progreso_id, progreso)

@router.delete("/{progreso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progreso(progreso_id: int, db: Session = Depends(get_db)):
    """Eliminar progreso"""
    service = ProgresoFisicoService(db)
    service.delete(progreso_id)