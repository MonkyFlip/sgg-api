"""Endpoints de Facturas"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id
from app.services.factura_service import FacturaService
from app.schemas.factura import FacturaCreate, FacturaResponse

router = APIRouter()

@router.post("/", response_model=FacturaResponse, status_code=status.HTTP_201_CREATED)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)):
    """Crear nueva factura"""
    service = FacturaService(db)
    return service.create(factura)

@router.get("/", response_model=List[FacturaResponse])
def get_facturas(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar facturas del gimnasio"""
    service = FacturaService(db)
    return service.get_by_gimnasio(gimnasio_id)

@router.get("/usuario/{usuario_id}", response_model=List[FacturaResponse])
def get_facturas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener facturas de un usuario"""
    service = FacturaService(db)
    return service.get_by_usuario(usuario_id)

@router.get("/{factura_id}", response_model=FacturaResponse)
def get_factura(factura_id: int, db: Session = Depends(get_db)):
    """Obtener factura por ID"""
    service = FacturaService(db)
    return service.get_by_id(factura_id)