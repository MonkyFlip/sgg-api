"""Dieta Entity"""
from dataclasses import dataclass
from datetime import date
from typing import Optional
from decimal import Decimal

@dataclass
class DietaEntity:
    """Entidad de dominio para Dieta"""
    id: Optional[int]
    nombre: str
    entrenador_id: int
    cliente_id: int
    fecha_inicio: date
    activo: bool = True
    fecha_fin: Optional[date] = None
    calorias_totales: Optional[int] = None
    proteinas_gramos: Optional[Decimal] = None
    carbohidratos_gramos: Optional[Decimal] = None
    grasas_gramos: Optional[Decimal] = None
    
    def esta_vigente(self) -> bool:
        """Verifica si la dieta está vigente"""
        if not self.activo:
            return False
        hoy = date.today()
        if hoy < self.fecha_inicio:
            return False
        if self.fecha_fin and hoy > self.fecha_fin:
            return False
        return True
    
    def calcular_macros_porcentaje(self) -> dict:
        """Calcula porcentaje de macronutrientes"""
        if not all([self.proteinas_gramos, self.carbohidratos_gramos, self.grasas_gramos]):
            return {}
        
        # 1g proteína = 4 cal, 1g carbs = 4 cal, 1g grasa = 9 cal
        calorias_proteinas = float(self.proteinas_gramos) * 4
        calorias_carbohidratos = float(self.carbohidratos_gramos) * 4
        calorias_grasas = float(self.grasas_gramos) * 9
        total = calorias_proteinas + calorias_carbohidratos + calorias_grasas
        
        if total == 0:
            return {}
        
        return {
            "proteinas": round((calorias_proteinas / total) * 100, 1),
            "carbohidratos": round((calorias_carbohidratos / total) * 100, 1),
            "grasas": round((calorias_grasas / total) * 100, 1)
        }