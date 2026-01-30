"""Producto Entity"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class ProductoEntity:
    """Entidad de dominio para Producto"""
    id: Optional[int]
    nombre: str
    gimnasio_id: int
    precio: Decimal
    stock_actual: int
    stock_minimo: int
    activo: bool = True
    categoria_id: Optional[int] = None
    
    def tiene_stock(self, cantidad: int = 1) -> bool:
        """Verifica si hay stock disponible"""
        return self.stock_actual >= cantidad
    
    def esta_bajo_stock(self) -> bool:
        """Verifica si está bajo stock mínimo"""
        return self.stock_actual <= self.stock_minimo
    
    def sin_stock(self) -> bool:
        """Verifica si no hay stock"""
        return self.stock_actual == 0
    
    def puede_vender(self, cantidad: int) -> bool:
        """Verifica si se puede vender la cantidad solicitada"""
        return self.activo and self.tiene_stock(cantidad)