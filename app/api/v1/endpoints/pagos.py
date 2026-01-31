"""Endpoints de Pagos"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db
from app.services.pago_service import PagoService
from app.schemas.pago import PagoCreate, PagoResponse

router = APIRouter()

@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def create_pago(pago: PagoCreate, db: Session = Depends(get_db)):
    """Registrar nuevo pago"""
    service = PagoService(db)
    return service.create(pago)

@router.get("/factura/{factura_id}", response_model=List[PagoResponse])
def get_pagos_factura(factura_id: int, db: Session = Depends(get_db)):
    """Obtener pagos de una factura"""
    service = PagoService(db)
    return service.get_by_factura(factura_id)

@router.get("/{pago_id}", response_model=PagoResponse)
def get_pago(pago_id: int, db: Session = Depends(get_db)):
    """Obtener pago por ID"""
    service = PagoService(db)
    return service.get_by_id(pago_id)