"""Membresía Entity"""
from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal

@dataclass
class MembresiaEntity:
    """Entidad de dominio para Membresía"""
    id: Optional[int]
    usuario_id: int
    fecha_inicio: date
    fecha_fin: date
    precio_pagado: Decimal
    estado: str
    
    @property
    def esta_activa(self) -> bool:
        """Verifica si la membresía está activa"""
        hoy = date.today()
        return self.estado == "ACTIVA" and self.fecha_inicio <= hoy <= self.fecha_fin
    
    @property
    def dias_restantes(self) -> int:
        """Calcula días restantes"""
        if not self.esta_activa:
            return 0
        return (self.fecha_fin - date.today()).days
    
    @property
    def dias_totales(self) -> int:
        """Calcula días totales de la membresía"""
        return (self.fecha_fin - self.fecha_inicio).days
    
    @property
    def porcentaje_usado(self) -> float:
        """Calcula porcentaje usado"""
        if self.dias_totales == 0:
            return 100.0
        dias_usados = (date.today() - self.fecha_inicio).days
        return round((dias_usados / self.dias_totales) * 100, 2)
    
    def esta_por_vencer(self, dias: int = 7) -> bool:
        """Verifica si está por vencer en N días"""
        return 0 < self.dias_restantes <= dias
    
    def esta_vencida(self) -> bool:
        """Verifica si está vencida"""
        return date.today() > self.fecha_fin