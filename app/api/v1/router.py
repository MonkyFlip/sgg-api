"""Router principal de la API V1"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    usuarios,
    gimnasios,
    roles,
    membresias,
    accesos,
    entrenadores,
    clases,
    reservas,
    productos,
    facturas,
    pagos,
    inventario,
    rutinas,
    dietas,
    progreso,
    notificaciones,
    reportes
)

api_router = APIRouter()

# Incluir todos los routers
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(gimnasios.router, prefix="/gimnasios", tags=["Gimnasios"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(membresias.router, prefix="/membresias", tags=["Membresías"])
api_router.include_router(accesos.router, prefix="/accesos", tags=["Accesos"])
api_router.include_router(entrenadores.router, prefix="/entrenadores", tags=["Entrenadores"])
api_router.include_router(clases.router, prefix="/clases", tags=["Clases"])
api_router.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
api_router.include_router(productos.router, prefix="/productos", tags=["Productos"])
api_router.include_router(facturas.router, prefix="/facturas", tags=["Facturas"])
api_router.include_router(pagos.router, prefix="/pagos", tags=["Pagos"])
api_router.include_router(inventario.router, prefix="/inventario", tags=["Inventario"])
api_router.include_router(rutinas.router, prefix="/rutinas", tags=["Rutinas"])
api_router.include_router(dietas.router, prefix="/dietas", tags=["Dietas"])
api_router.include_router(progreso.router, prefix="/progreso", tags=["Progreso Físico"])
api_router.include_router(notificaciones.router, prefix="/notificaciones", tags=["Notificaciones"])
api_router.include_router(reportes.router, prefix="/reportes", tags=["Reportes"])