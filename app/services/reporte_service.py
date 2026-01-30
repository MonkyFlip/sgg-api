"""Service de Reportes y Análisis"""
from typing import List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract

from app.repositories.usuario import UsuarioRepository
from app.repositories.membresia import MembresiaRepository
from app.repositories.acceso import AccesoRepository
from app.repositories.factura import FacturaRepository
from app.repositories.producto import ProductoRepository
from app.repositories.clase import ClaseRepository
from app.repositories.reserva import ReservaRepository
from app.core.constants import EstadoMembresiaEnum, EstadoFacturaEnum


class ReporteService:
    """Servicio para generar reportes y análisis del gimnasio"""
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.membresia_repo = MembresiaRepository(db)
        self.acceso_repo = AccesoRepository(db)
        self.factura_repo = FacturaRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.clase_repo = ClaseRepository(db)
        self.reserva_repo = ReservaRepository(db)
    
    # ========================================
    # REPORTES DE USUARIOS
    # ========================================
    
    def reporte_usuarios(self, gimnasio_id: int) -> Dict[str, Any]:
        """
        Genera reporte general de usuarios.
        
        Args:
            gimnasio_id: ID del gimnasio
            
        Returns:
            Diccionario con estadísticas de usuarios
        """
        usuarios = self.usuario_repo.get_by_gimnasio(gimnasio_id, skip=0, limit=10000)
        
        total = len(usuarios)
        activos = len([u for u in usuarios if u.activo])
        inactivos = total - activos
        
        # Por rol
        clientes = len([u for u in usuarios if u.es_cliente()])
        entrenadores = len([u for u in usuarios if u.es_entrenador()])
        staff = len([u for u in usuarios if u.es_staff()])
        admins = len([u for u in usuarios if u.es_admin()])
        
        # Por género
        hombres = len([u for u in usuarios if u.genero and u.genero.value == 'M'])
        mujeres = len([u for u in usuarios if u.genero and u.genero.value == 'F'])
        otros = len([u for u in usuarios if u.genero and u.genero.value == 'OTRO'])
        sin_genero = len([u for u in usuarios if not u.genero])
        
        return {
            "total_usuarios": total,
            "usuarios_activos": activos,
            "usuarios_inactivos": inactivos,
            "por_rol": {
                "clientes": clientes,
                "entrenadores": entrenadores,
                "staff": staff,
                "administradores": admins
            },
            "por_genero": {
                "hombres": hombres,
                "mujeres": mujeres,
                "otros": otros,
                "sin_especificar": sin_genero
            }
        }
    
    # ========================================
    # REPORTES DE MEMBRESÍAS
    # ========================================
    
    def reporte_membresias(self, gimnasio_id: int) -> Dict[str, Any]:
        """
        Genera reporte de membresías.
        
        Args:
            gimnasio_id: ID del gimnasio
            
        Returns:
            Diccionario con estadísticas de membresías
        """
        from app.models.membresia import Membresia
        
        # Total de membresías
        total = self.db.query(Membresia).join(Membresia.usuario).filter(
            Membresia.usuario.has(gimnasio_id=gimnasio_id)
        ).count()
        
        # Por estado
        activas = self.db.query(Membresia).join(Membresia.usuario).filter(
            and_(
                Membresia.usuario.has(gimnasio_id=gimnasio_id),
                Membresia.estado == EstadoMembresiaEnum.ACTIVA
            )
        ).count()
        
        vencidas = self.db.query(Membresia).join(Membresia.usuario).filter(
            and_(
                Membresia.usuario.has(gimnasio_id=gimnasio_id),
                Membresia.estado == EstadoMembresiaEnum.VENCIDA
            )
        ).count()
        
        canceladas = self.db.query(Membresia).join(Membresia.usuario).filter(
            and_(
                Membresia.usuario.has(gimnasio_id=gimnasio_id),
                Membresia.estado == EstadoMembresiaEnum.CANCELADA
            )
        ).count()
        
        # Próximas a vencer (7 días)
        proximas_vencer = len(self.membresia_repo.get_proximas_vencer(dias=7))
        
        return {
            "total_membresias": total,
            "por_estado": {
                "activas": activas,
                "vencidas": vencidas,
                "canceladas": canceladas
            },
            "proximas_vencer_7_dias": proximas_vencer,
            "tasa_renovacion": round((activas / total * 100), 2) if total > 0 else 0
        }
    
    # ========================================
    # REPORTES DE ASISTENCIA
    # ========================================
    
    def reporte_asistencia(
        self,
        gimnasio_id: int,
        fecha_inicio: date = None,
        fecha_fin: date = None
    ) -> Dict[str, Any]:
        """
        Genera reporte de asistencia.
        
        Args:
            gimnasio_id: ID del gimnasio
            fecha_inicio: Fecha de inicio (por defecto: hace 30 días)
            fecha_fin: Fecha de fin (por defecto: hoy)
            
        Returns:
            Diccionario con estadísticas de asistencia
        """
        if not fecha_fin:
            fecha_fin = date.today()
        if not fecha_inicio:
            fecha_inicio = fecha_fin - timedelta(days=30)
        
        from app.models.acceso import Acceso
        
        # Total de accesos en el período
        total_accesos = self.db.query(Acceso).filter(
            and_(
                Acceso.gimnasio_id == gimnasio_id,
                func.date(Acceso.fecha_hora_entrada) >= fecha_inicio,
                func.date(Acceso.fecha_hora_entrada) <= fecha_fin
            )
        ).count()
        
        # Promedio diario
        dias_periodo = (fecha_fin - fecha_inicio).days + 1
        promedio_diario = round(total_accesos / dias_periodo, 2) if dias_periodo > 0 else 0
        
        # Usuarios únicos
        usuarios_unicos = self.db.query(func.count(func.distinct(Acceso.usuario_id))).filter(
            and_(
                Acceso.gimnasio_id == gimnasio_id,
                func.date(Acceso.fecha_hora_entrada) >= fecha_inicio,
                func.date(Acceso.fecha_hora_entrada) <= fecha_fin
            )
        ).scalar()
        
        # Día con más asistencia
        dia_mas_asistencia = self.db.query(
            func.date(Acceso.fecha_hora_entrada).label('fecha'),
            func.count(Acceso.id).label('total')
        ).filter(
            and_(
                Acceso.gimnasio_id == gimnasio_id,
                func.date(Acceso.fecha_hora_entrada) >= fecha_inicio,
                func.date(Acceso.fecha_hora_entrada) <= fecha_fin
            )
        ).group_by(func.date(Acceso.fecha_hora_entrada)).order_by(func.count(Acceso.id).desc()).first()
        
        return {
            "periodo": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "dias": dias_periodo
            },
            "total_accesos": total_accesos,
            "promedio_diario": promedio_diario,
            "usuarios_unicos": usuarios_unicos,
            "dia_mas_concurrido": {
                "fecha": dia_mas_asistencia.fecha if dia_mas_asistencia else None,
                "total": dia_mas_asistencia.total if dia_mas_asistencia else 0
            }
        }
    
    # ========================================
    # REPORTES FINANCIEROS
    # ========================================
    
    def reporte_financiero(
        self,
        gimnasio_id: int,
        fecha_inicio: date = None,
        fecha_fin: date = None
    ) -> Dict[str, Any]:
        """
        Genera reporte financiero.
        
        Args:
            gimnasio_id: ID del gimnasio
            fecha_inicio: Fecha de inicio (por defecto: primer día del mes)
            fecha_fin: Fecha de fin (por defecto: hoy)
            
        Returns:
            Diccionario con estadísticas financieras
        """
        if not fecha_fin:
            fecha_fin = date.today()
        if not fecha_inicio:
            fecha_inicio = date(fecha_fin.year, fecha_fin.month, 1)
        
        from app.models.factura import Factura
        
        # Facturas del período
        facturas = self.db.query(Factura).filter(
            and_(
                Factura.gimnasio_id == gimnasio_id,
                func.date(Factura.fecha_emision) >= fecha_inicio,
                func.date(Factura.fecha_emision) <= fecha_fin
            )
        ).all()
        
        # Totales
        total_facturado = sum(float(f.total) for f in facturas)
        total_pagado = sum(float(f.total) for f in facturas if f.estado == EstadoFacturaEnum.PAGADA)
        total_pendiente = sum(float(f.total) for f in facturas if f.estado == EstadoFacturaEnum.PENDIENTE)
        
        # Por tipo
        membresias = sum(float(f.total) for f in facturas if f.tipo.value == 'MEMBRESIA')
        productos = sum(float(f.total) for f in facturas if f.tipo.value == 'PRODUCTO')
        servicios = sum(float(f.total) for f in facturas if f.tipo.value == 'SERVICIO')
        
        return {
            "periodo": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            },
            "total_facturas": len(facturas),
            "totales": {
                "facturado": round(total_facturado, 2),
                "pagado": round(total_pagado, 2),
                "pendiente": round(total_pendiente, 2)
            },
            "por_tipo": {
                "membresias": round(membresias, 2),
                "productos": round(productos, 2),
                "servicios": round(servicios, 2)
            },
            "tasa_cobranza": round((total_pagado / total_facturado * 100), 2) if total_facturado > 0 else 0
        }
    
    # ========================================
    # REPORTES DE CLASES
    # ========================================
    
    def reporte_clases(self, gimnasio_id: int) -> Dict[str, Any]:
        """
        Genera reporte de clases grupales.
        
        Args:
            gimnasio_id: ID del gimnasio
            
        Returns:
            Diccionario con estadísticas de clases
        """
        clases = self.clase_repo.get_by_gimnasio(gimnasio_id, skip=0, limit=1000)
        
        total_clases = len(clases)
        clases_activas = len([c for c in clases if c.activo])
        
        # Capacidad total
        capacidad_total = sum(c.capacidad_maxima for c in clases if c.activo)
        
        # Clases más populares (por reservas) - requeriría join con reservas
        # Por ahora retornamos estructura básica
        
        return {
            "total_clases": total_clases,
            "clases_activas": clases_activas,
            "capacidad_total": capacidad_total,
            "promedio_capacidad": round(capacidad_total / clases_activas, 2) if clases_activas > 0 else 0
        }
    
    # ========================================
    # REPORTES DE PRODUCTOS
    # ========================================
    
    def reporte_inventario(self, gimnasio_id: int) -> Dict[str, Any]:
        """
        Genera reporte de inventario de productos.
        
        Args:
            gimnasio_id: ID del gimnasio
            
        Returns:
            Diccionario con estadísticas de inventario
        """
        productos = self.producto_repo.get_by_gimnasio(gimnasio_id, skip=0, limit=10000)
        productos_activos = [p for p in productos if p.activo]
        
        # Valor del inventario
        valor_total = sum(float(p.precio * p.stock_actual) for p in productos_activos)
        
        # Productos bajo stock
        bajo_stock = self.producto_repo.get_bajo_stock(gimnasio_id)
        
        # Productos sin stock
        sin_stock = len([p for p in productos_activos if p.stock_actual == 0])
        
        return {
            "total_productos": len(productos),
            "productos_activos": len(productos_activos),
            "valor_inventario": round(valor_total, 2),
            "productos_bajo_stock": len(bajo_stock),
            "productos_sin_stock": sin_stock,
            "items_totales": sum(p.stock_actual for p in productos_activos)
        }
    
    # ========================================
    # DASHBOARD GENERAL
    # ========================================
    
    def dashboard_general(self, gimnasio_id: int) -> Dict[str, Any]:
        """
        Genera resumen para dashboard principal.
        
        Args:
            gimnasio_id: ID del gimnasio
            
        Returns:
            Diccionario con métricas principales
        """
        # Usuarios
        total_usuarios = self.usuario_repo.count({"gimnasio_id": gimnasio_id})
        usuarios_activos = self.usuario_repo.get_activos(gimnasio_id, skip=0, limit=10000)
        
        # Membresías
        membresias_activas = self.db.query(func.count()).select_from(
            self.db.query(self.membresia_repo.model).join(
                self.membresia_repo.model.usuario
            ).filter(
                and_(
                    self.membresia_repo.model.usuario.has(gimnasio_id=gimnasio_id),
                    self.membresia_repo.model.estado == EstadoMembresiaEnum.ACTIVA
                )
            ).subquery()
        ).scalar()
        
        # Usuarios en gimnasio ahora
        usuarios_presentes = len(self.acceso_repo.get_usuarios_en_gimnasio(gimnasio_id))
        
        # Ingresos del mes
        hoy = date.today()
        primer_dia_mes = date(hoy.year, hoy.month, 1)
        reporte_fin = self.reporte_financiero(gimnasio_id, primer_dia_mes, hoy)
        
        return {
            "usuarios": {
                "total": total_usuarios,
                "activos": len(usuarios_activos),
                "presentes_ahora": usuarios_presentes
            },
            "membresias_activas": membresias_activas,
            "ingresos_mes": reporte_fin["totales"]["pagado"],
            "fecha_actualizacion": datetime.now()
        }