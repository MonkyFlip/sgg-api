"""Endpoints de Productos"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_db, get_gimnasio_id
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse

router = APIRouter()

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear nuevo producto"""
    service = ProductoService(db)
    return service.create(producto)

@router.get("/", response_model=List[ProductoResponse])
def get_productos(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar productos del gimnasio"""
    service = ProductoService(db)
    return service.get_by_gimnasio(gimnasio_id)

@router.get("/bajo-stock", response_model=List[ProductoResponse])
def get_productos_bajo_stock(
    gimnasio_id: int = Depends(get_gimnasio_id),
    db: Session = Depends(get_db)
):
    """Listar productos con stock bajo"""
    service = ProductoService(db)
    return service.get_bajo_stock(gimnasio_id)

@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener producto por ID"""
    service = ProductoService(db)
    return service.get_by_id(producto_id)

@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar producto"""
    service = ProductoService(db)
    return service.update(producto_id, producto)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    """Eliminar producto"""
    service = ProductoService(db)
    service.delete(producto_id)