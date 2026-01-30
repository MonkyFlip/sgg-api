"""
Base Service
Servicio base con operaciones comunes para todos los servicios
"""

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Servicio base con operaciones CRUD genéricas.
    
    Uso:
    ```python
    class UsuarioService(BaseService[Usuario, UsuarioCreate, UsuarioUpdate]):
        def __init__(self, db: Session):
            super().__init__(UsuarioRepository(db))
    ```
    """
    
    def __init__(self, repository: BaseRepository[ModelType]):
        """
        Inicializa el servicio.
        
        Args:
            repository: Repository del modelo
        """
        self.repo = repository
    
    def create(self, data: CreateSchemaType) -> ModelType:
        """
        Crea un nuevo registro.
        
        Args:
            data: Schema con los datos a crear
            
        Returns:
            Registro creado
        """
        obj_data = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        return self.repo.create(obj_data)
    
    def get_by_id(self, id: int) -> ModelType:
        """
        Obtiene un registro por ID.
        
        Args:
            id: ID del registro
            
        Returns:
            Registro encontrado
            
        Raises:
            HTTPException: Si el registro no existe
        """
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self._get_model_name()} no encontrado"
            )
        return obj
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None
    ) -> List[ModelType]:
        """
        Obtiene todos los registros con paginación.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            filters: Filtros opcionales
            
        Returns:
            Lista de registros
        """
        return self.repo.get_all(skip=skip, limit=limit, filters=filters)
    
    def update(self, id: int, data: UpdateSchemaType) -> ModelType:
        """
        Actualiza un registro existente.
        
        Args:
            id: ID del registro
            data: Schema con los datos a actualizar
            
        Returns:
            Registro actualizado
            
        Raises:
            HTTPException: Si el registro no existe
        """
        # Verificar que existe
        self.get_by_id(id)
        
        # Actualizar
        update_data = data.model_dump(exclude_unset=True) if hasattr(data, 'model_dump') else data.dict(exclude_unset=True)
        updated = self.repo.update(id, update_data)
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self._get_model_name()} no encontrado"
            )
        
        return updated
    
    def delete(self, id: int) -> bool:
        """
        Elimina un registro.
        
        Args:
            id: ID del registro
            
        Returns:
            True si se eliminó exitosamente
            
        Raises:
            HTTPException: Si el registro no existe
        """
        if not self.repo.delete(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self._get_model_name()} no encontrado"
            )
        return True
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        Cuenta registros con filtros opcionales.
        
        Args:
            filters: Filtros opcionales
            
        Returns:
            Número de registros
        """
        return self.repo.count(filters=filters)
    
    def exists(self, id: int) -> bool:
        """
        Verifica si existe un registro.
        
        Args:
            id: ID del registro
            
        Returns:
            True si existe
        """
        return self.repo.exists(id)
    
    def _get_model_name(self) -> str:
        """
        Obtiene el nombre del modelo para mensajes de error.
        
        Returns:
            Nombre del modelo
        """
        if hasattr(self.repo, 'model'):
            return self.repo.model.__name__
        return "Registro"
    
    # ========================================
    # MÉTODOS DE VALIDACIÓN COMUNES
    # ========================================
    
    def validate_unique_field(
        self,
        field_name: str,
        field_value: Any,
        exclude_id: Optional[int] = None
    ) -> None:
        """
        Valida que un campo sea único.
        
        Args:
            field_name: Nombre del campo
            field_value: Valor del campo
            exclude_id: ID a excluir de la validación (para updates)
            
        Raises:
            HTTPException: Si el valor ya existe
        """
        filters = {field_name: field_value}
        existing = self.repo.get_one_by_filters(**filters)
        
        if existing and (exclude_id is None or existing.id != exclude_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El {field_name} ya está en uso"
            )
    
    def validate_belongs_to_gym(self, obj_id: int, gimnasio_id: int) -> None:
        """
        Valida que un registro pertenezca a un gimnasio específico.
        
        Args:
            obj_id: ID del registro
            gimnasio_id: ID del gimnasio
            
        Raises:
            HTTPException: Si el registro no pertenece al gimnasio
        """
        obj = self.get_by_id(obj_id)
        
        if hasattr(obj, 'gimnasio_id') and obj.gimnasio_id != gimnasio_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este recurso"
            )
    
    def validate_active(self, id: int) -> None:
        """
        Valida que un registro esté activo.
        
        Args:
            id: ID del registro
            
        Raises:
            HTTPException: Si el registro no está activo
        """
        obj = self.get_by_id(id)
        
        if hasattr(obj, 'activo') and not obj.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{self._get_model_name()} no está activo"
            )
    
    # ========================================
    # MÉTODOS DE SOFT DELETE
    # ========================================
    
    def soft_delete(self, id: int) -> ModelType:
        """
        Elimina un registro de forma lógica (soft delete).
        
        Args:
            id: ID del registro
            
        Returns:
            Registro actualizado con activo=False
        """
        return self.repo.update(id, {"activo": False})
    
    def restore(self, id: int) -> ModelType:
        """
        Restaura un registro eliminado lógicamente.
        
        Args:
            id: ID del registro
            
        Returns:
            Registro actualizado con activo=True
        """
        return self.repo.update(id, {"activo": True})