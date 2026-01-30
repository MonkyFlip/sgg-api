"""Interface de Repository de Gimnasio"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.interfaces.repository_interface import IRepository

class IGimnasioRepository(IRepository):
    """
    Interface para el repositorio de gimnasios.
    Define operaciones específicas de gimnasios.
    """
    
    @abstractmethod
    def get_by_codigo(self, codigo_unico: str) -> Optional[any]:
        """
        Obtiene un gimnasio por código único.
        
        Args:
            codigo_unico: Código único del gimnasio
            
        Returns:
            Gimnasio o None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[any]:
        """
        Obtiene un gimnasio por email.
        
        Args:
            email: Email del gimnasio
            
        Returns:
            Gimnasio o None si no existe
        """
        pass
    
    @abstractmethod
    def get_activos(self, skip: int = 0, limit: int = 100) -> List:
        """
        Obtiene gimnasios activos.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de gimnasios activos
        """
        pass