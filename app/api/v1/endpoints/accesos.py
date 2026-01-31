"""Endpoints de Accesos"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id
from app.services.acceso_service import AccesoService
from app.schemas.acceso import AccesoResponse, RegistrarEntrada, RegistrarSalida

router = APIRouter()

@router.post("/entrada", response_model=AccesoResponse, status_code=status.HTTP_201_CREATED)
def registrar_entrada(
    entrada: RegistrarEntrada,
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Registrar entrada al gimnasio"""
    service = AccesoService(db)
    return service.registrar_entrada(entrada, gimnasio_id)

@router.post("/salida")
def registrar_salida(salida: RegistrarSalida, db: Session = Depends(get_db)):
    """Registrar salida del gimnasio"""
    service = AccesoService(db)
    return service.registrar_salida(salida)

@router.get("/presentes", response_model=List[AccesoResponse])
def get_usuarios_presentes(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Obtener usuarios presentes en el gimnasio"""
    service = AccesoService(db)
    return service.get_usuarios_en_gimnasio(gimnasio_id)

@router.get("/usuario/{usuario_id}", response_model=List[AccesoResponse])
def get_accesos_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener historial de accesos de un usuario"""
    service = AccesoService(db)
    return service.get_by_usuario(usuario_id)