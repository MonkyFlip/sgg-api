"""Endpoints de Inventario"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id
from app.services.inventario_service import InventarioService
from app.schemas.inventario import InventarioCreate, InventarioUpdate, InventarioResponse

router = APIRouter()

@router.post("/", response_model=InventarioResponse, status_code=status.HTTP_201_CREATED)
def create_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    """Crear nuevo item de inventario"""
    service = InventarioService(db)
    return service.create(inventario)

@router.get("/", response_model=List[InventarioResponse])
def get_inventario(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar inventario del gimnasio"""
    service = InventarioService(db)
    return service.get_by_gimnasio(gimnasio_id)

@router.get("/mantenimiento", response_model=List[InventarioResponse])
def get_requiere_mantenimiento(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar items que requieren mantenimiento"""
    service = InventarioService(db)
    return service.get_requiere_mantenimiento(gimnasio_id)

@router.get("/{item_id}", response_model=InventarioResponse)
def get_item_inventario(item_id: int, db: Session = Depends(get_db)):
    """Obtener item de inventario por ID"""
    service = InventarioService(db)
    return service.get_by_id(item_id)

@router.put("/{item_id}", response_model=InventarioResponse)
def update_inventario(
    item_id: int,
    inventario: InventarioUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar item de inventario"""
    service = InventarioService(db)
    return service.update(item_id, inventario)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventario(item_id: int, db: Session = Depends(get_db)):
    """Eliminar item de inventario"""
    service = InventarioService(db)
    service.delete(item_id)