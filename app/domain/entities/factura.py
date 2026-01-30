"""Factura Entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class FacturaEntity:
    """Entidad de dominio para Factura"""
    id: Optional[int]
    numero_factura: str
    gimnasio_id: int
    usuario_id: int
    subtotal: Decimal
    total: Decimal
    estado: str
    fecha_emision: datetime
    impuestos: Decimal = Decimal("0")
    descuentos: Decimal = Decimal("0")
    fecha_pago: Optional[datetime] = None
    
    @property
    def esta_pagada(self) -> bool:
        """Verifica si está pagada"""
        return self.estado == "PAGADA"
    
    @property
    def esta_pendiente(self) -> bool:
        """Verifica si está pendiente"""
        return self.estado == "PENDIENTE"
    
    def calcular_total(self) -> Decimal:
        """Calcula el total de la factura"""
        return self.subtotal + self.impuestos - self.descuentos
    
    def validar_totales(self) -> bool:
        """Valida que los totales sean correctos"""
        return abs(self.calcular_total() - self.total) < Decimal("0.01")
    
    def dias_desde_emision(self) -> int:
        """Calcula días desde emisión"""
        return (datetime.now() - self.fecha_emision).days