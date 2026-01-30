"""Interface Base de Repository"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    """
    Interface base para repositorios.
    Define el contrato que deben cumplir todos los repositorios.
    """
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtiene una entidad por ID.
        
        Args:
            id: ID de la entidad
            
        Returns:
            Entidad o None si no existe
        """
        pass
    
    @abstractmethod
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None
    ) -> List[T]:
        """
        Obtiene todas las entidades con paginación.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            filters: Filtros opcionales
            
        Returns:
            Lista de entidades
        """
        pass
    
    @abstractmethod
    def create(self, obj_data: Dict[str, Any]) -> T:
        """
        Crea una nueva entidad.
        
        Args:
            obj_data: Datos de la entidad
            
        Returns:
            Entidad creada
        """
        pass
    
    @abstractmethod
    def update(self, id: int, obj_data: Dict[str, Any]) -> Optional[T]:
        """
        Actualiza una entidad existente.
        
        Args:
            id: ID de la entidad
            obj_data: Datos a actualizar
            
        Returns:
            Entidad actualizada o None si no existe
        """
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Elimina una entidad.
        
        Args:
            id: ID de la entidad
            
        Returns:
            True si se eliminó, False si no existe
        """
        pass
    
    @abstractmethod
    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        Cuenta entidades con filtros opcionales.
        
        Args:
            filters: Filtros opcionales
            
        Returns:
            Número de entidades
        """
        pass
    
    @abstractmethod
    def exists(self, id: int) -> bool:
        """
        Verifica si existe una entidad.
        
        Args:
            id: ID de la entidad
            
        Returns:
            True si existe
        """
        pass