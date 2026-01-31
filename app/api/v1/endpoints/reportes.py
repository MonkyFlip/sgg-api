"""Endpoints de Reportes y Análisis"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.api.dependencies import get_db, get_gimnasio_id, require_admin
from app.services.reporte_service import ReporteService

router = APIRouter()

@router.get("/usuarios")
def reporte_usuarios(
    gimnasio_id: int = Depends(get_gimnasio_id),
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte de usuarios del gimnasio"""
    service = ReporteService(db)
    return service.reporte_usuarios(gimnasio_id)

@router.get("/membresias")
def reporte_membresias(
    gimnasio_id: int = Depends(get_gimnasio_id),
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte de membresías"""
    service = ReporteService(db)
    return service.reporte_membresias(gimnasio_id)

@router.get("/asistencia")
def reporte_asistencia(
    gimnasio_id: int = Depends(get_gimnasio_id),
    fecha_inicio: date = None,
    fecha_fin: date = None,
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte de asistencia"""
    service = ReporteService(db)
    return service.reporte_asistencia(gimnasio_id, fecha_inicio, fecha_fin)

@router.get("/financiero")
def reporte_financiero(
    gimnasio_id: int = Depends(get_gimnasio_id),
    fecha_inicio: date = None,
    fecha_fin: date = None,
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte financiero"""
    service = ReporteService(db)
    return service.reporte_financiero(gimnasio_id, fecha_inicio, fecha_fin)

@router.get("/clases")
def reporte_clases(
    gimnasio_id: int = Depends(get_gimnasio_id),
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte de clases grupales"""
    service = ReporteService(db)
    return service.reporte_clases(gimnasio_id)

@router.get("/inventario")
def reporte_inventario(
    gimnasio_id: int = Depends(get_gimnasio_id),
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Reporte de inventario"""
    service = ReporteService(db)
    return service.reporte_inventario(gimnasio_id)

@router.get("/dashboard")
def dashboard_general(
    gimnasio_id: int = Depends(get_gimnasio_id),
    admin = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Dashboard general con métricas principales"""
    service = ReporteService(db)
    return service.dashboard_general(gimnasio_id)