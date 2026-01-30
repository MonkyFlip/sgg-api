"""Interface de Repository de Usuario"""
from abc import abstractmethod
from typing import Optional, List
from app.domain.interfaces.repository_interface import IRepository

class IUsuarioRepository(IRepository):
    """
    Interface para el repositorio de usuarios.
    Define operaciones específicas de usuarios.
    """
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[any]:
        """
        Obtiene un usuario por email.
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario o None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_gimnasio(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List:
        """
        Obtiene usuarios de un gimnasio.
        
        Args:
            gimnasio_id: ID del gimnasio
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de usuarios
        """
        pass
    
    @abstractmethod
    def get_clientes(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List:
        """
        Obtiene clientes de un gimnasio.
        
        Args:
            gimnasio_id: ID del gimnasio
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de clientes
        """
        pass
    
    @abstractmethod
    def get_entrenadores(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List:
        """
        Obtiene entrenadores de un gimnasio.
        
        Args:
            gimnasio_id: ID del gimnasio
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de entrenadores
        """
        pass
    
    @abstractmethod
    def get_activos(self, gimnasio_id: int, skip: int = 0, limit: int = 100) -> List:
        """
        Obtiene usuarios activos de un gimnasio.
        
        Args:
            gimnasio_id: ID del gimnasio
            skip: Número de registros a saltar
            limit: Número máximo de registros
            
        Returns:
            Lista de usuarios activos
        """
        pass