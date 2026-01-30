"""Utilidades de paginación"""
from typing import List, Generic, TypeVar, Optional
from pydantic import BaseModel
from math import ceil

T = TypeVar('T')

class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    page: int = 1
    page_size: int = 20
    
    @property
    def skip(self) -> int:
        """Calcula el número de registros a saltar"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """Alias para page_size"""
        return self.page_size
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    class Config:
        from_attributes = True

class Paginator(Generic[T]):
    """Clase para manejar paginación"""
    
    def __init__(self, items: List[T], total: int, page: int = 1, page_size: int = 20):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = ceil(total / page_size) if page_size > 0 else 0
    
    @property
    def has_next(self) -> bool:
        """Verifica si hay página siguiente"""
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        """Verifica si hay página anterior"""
        return self.page > 1
    
    def to_response(self) -> PaginatedResponse[T]:
        """Convierte a respuesta paginada"""
        return PaginatedResponse(
            items=self.items,
            total=self.total,
            page=self.page,
            page_size=self.page_size,
            total_pages=self.total_pages,
            has_next=self.has_next,
            has_prev=self.has_prev
        )

def paginar(
    items: List[T],
    total: int,
    page: int = 1,
    page_size: int = 20
) -> PaginatedResponse[T]:
    """
    Función helper para paginar resultados.
    
    Args:
        items: Lista de items de la página actual
        total: Total de items en la base de datos
        page: Número de página (empieza en 1)
        page_size: Items por página
        
    Returns:
        Respuesta paginada
    """
    paginator = Paginator(items, total, page, page_size)
    return paginator.to_response()