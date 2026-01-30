"""
Repository Base
Clase base para todos los repositorios con operaciones CRUD genéricas
"""

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Repository base con operaciones CRUD genéricas.
    
    Uso:
    ```python
    class UsuarioRepository(BaseRepository[Usuario]):
        def __init__(self, db: Session):
            super().__init__(Usuario, db)
    ```
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Inicializa el repository.
        
        Args:
            model: Clase del modelo SQLAlchemy
            db: Sesión de base de datos
        """
        self.model = model
        self.db = db
    
    # ========================================
    # OPERACIONES CRUD BÁSICAS
    # ========================================
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Obtiene un registro por ID.
        
        Args:
            id: ID del registro
            
        Returns:
            Registro o None si no existe
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None,
        order_by: str = None,
        order_desc: bool = False
    ) -> List[ModelType]:
        """
        Obtiene todos los registros con paginación y filtros opcionales.
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            filters: Diccionario de filtros {campo: valor}
            order_by: Campo por el cual ordenar
            order_desc: Si ordenar descendente
            
        Returns:
            Lista de registros
        """
        query = self.db.query(self.model)
        
        # Aplicar filtros
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
        
        # Aplicar ordenamiento
        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            query = query.order_by(desc(order_column) if order_desc else asc(order_column))
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_filters(self, **filters) -> List[ModelType]:
        """
        Obtiene registros por filtros múltiples.
        
        Args:
            **filters: Filtros como keyword arguments
            
        Returns:
            Lista de registros que coinciden con los filtros
        """
        query = self.db.query(self.model)
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        return query.all()
    
    def get_one_by_filters(self, **filters) -> Optional[ModelType]:
        """
        Obtiene un único registro por filtros.
        
        Args:
            **filters: Filtros como keyword arguments
            
        Returns:
            Primer registro que coincide o None
        """
        query = self.db.query(self.model)
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        return query.first()
    
    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        """
        Crea un nuevo registro.
        
        Args:
            obj_data: Diccionario con los datos del registro
            
        Returns:
            Registro creado
        """
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, id: int, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """
        Actualiza un registro existente.
        
        Args:
            id: ID del registro a actualizar
            obj_data: Diccionario con los datos a actualizar
            
        Returns:
            Registro actualizado o None si no existe
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        
        for field, value in obj_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, id: int) -> bool:
        """
        Elimina un registro.
        
        Args:
            id: ID del registro a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        Cuenta los registros con filtros opcionales.
        
        Args:
            filters: Diccionario de filtros {campo: valor}
            
        Returns:
            Número de registros
        """
        query = self.db.query(self.model)
        
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)
        
        return query.count()
    
    def exists(self, id: int) -> bool:
        """
        Verifica si existe un registro con el ID dado.
        
        Args:
            id: ID a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        return self.db.query(self.model).filter(self.model.id == id).count() > 0
    
    def exists_by_filters(self, **filters) -> bool:
        """
        Verifica si existe un registro con los filtros dados.
        
        Args:
            **filters: Filtros como keyword arguments
            
        Returns:
            True si existe, False en caso contrario
        """
        query = self.db.query(self.model)
        
        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        
        return query.count() > 0
    
    # ========================================
    # OPERACIONES ADICIONALES
    # ========================================
    
    def bulk_create(self, objects_data: List[Dict[str, Any]]) -> List[ModelType]:
        """
        Crea múltiples registros en una sola operación.
        
        Args:
            objects_data: Lista de diccionarios con datos
            
        Returns:
            Lista de registros creados
        """
        db_objects = [self.model(**obj_data) for obj_data in objects_data]
        self.db.bulk_save_objects(db_objects)
        self.db.commit()
        return db_objects
    
    def bulk_update(self, updates: List[Dict[str, Any]]) -> int:
        """
        Actualiza múltiples registros en una sola operación.
        
        Args:
            updates: Lista de diccionarios con 'id' y datos a actualizar
            
        Returns:
            Número de registros actualizados
        """
        count = 0
        for update_data in updates:
            obj_id = update_data.pop('id', None)
            if obj_id and self.update(obj_id, update_data):
                count += 1
        return count
    
    def get_or_create(self, defaults: Dict[str, Any] = None, **filters) -> tuple[ModelType, bool]:
        """
        Obtiene un registro o lo crea si no existe.
        
        Args:
            defaults: Valores adicionales para crear el registro
            **filters: Filtros para buscar el registro
            
        Returns:
            Tupla (registro, creado) donde creado es True si se creó
        """
        instance = self.get_one_by_filters(**filters)
        
        if instance:
            return instance, False
        
        # Crear nuevo registro
        create_data = {**filters}
        if defaults:
            create_data.update(defaults)
        
        instance = self.create(create_data)
        return instance, True