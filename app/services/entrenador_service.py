"""Service de Entrenador"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, timedelta

from app.repositories.usuario import UsuarioRepository
from app.repositories.entrenador_cliente import EntrenadorClienteRepository
from app.repositories.rutina import RutinaRepository
from app.repositories.dieta import DietaRepository
from app.repositories.clase import ClaseRepository
from app.models.usuario import Usuario


class EntrenadorService:
    """Servicio especializado para operaciones de entrenadores"""
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)
        self.entrenador_cliente_repo = EntrenadorClienteRepository(db)
        self.rutina_repo = RutinaRepository(db)
        self.dieta_repo = DietaRepository(db)
        self.clase_repo = ClaseRepository(db)
    
    # ========================================
    # GESTIÓN DE CLIENTES
    # ========================================
    
    def get_mis_clientes(self, entrenador_id: int, activo: bool = True) -> List[Usuario]:
        """
        Obtiene los clientes asignados a un entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            activo: Filtrar solo relaciones activas
            
        Returns:
            Lista de clientes
        """
        # Verificar que sea entrenador
        entrenador = self.usuario_repo.get_by_id(entrenador_id)
        if not entrenador or not entrenador.es_entrenador():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario no es entrenador"
            )
        
        relaciones = self.entrenador_cliente_repo.get_clientes_entrenador(entrenador_id, activo)
        clientes = [self.usuario_repo.get_by_id(rel.cliente_id) for rel in relaciones]
        return [c for c in clientes if c is not None]
    
    def asignar_cliente(self, entrenador_id: int, cliente_id: int, notas: str = None) -> bool:
        """
        Asigna un cliente a un entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            cliente_id: ID del cliente
            notas: Notas de la asignación
            
        Returns:
            True si se asignó exitosamente
        """
        # Verificar entrenador
        entrenador = self.usuario_repo.get_by_id(entrenador_id)
        if not entrenador or not entrenador.es_entrenador():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario no es entrenador"
            )
        
        # Verificar cliente
        cliente = self.usuario_repo.get_by_id(cliente_id)
        if not cliente or not cliente.es_cliente():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario no es cliente"
            )
        
        # Verificar mismo gimnasio
        if entrenador.gimnasio_id != cliente.gimnasio_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cliente y entrenador deben pertenecer al mismo gimnasio"
            )
        
        # Verificar si ya existe relación
        if self.entrenador_cliente_repo.existe_relacion(entrenador_id, cliente_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El cliente ya está asignado a este entrenador"
            )
        
        # Crear relación
        self.entrenador_cliente_repo.create({
            "entrenador_id": entrenador_id,
            "cliente_id": cliente_id,
            "fecha_asignacion": date.today(),
            "notas": notas,
            "activo": True
        })
        
        return True
    
    def desasignar_cliente(self, entrenador_id: int, cliente_id: int) -> bool:
        """
        Desasigna un cliente de un entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            cliente_id: ID del cliente
            
        Returns:
            True si se desasignó exitosamente
        """
        relaciones = self.entrenador_cliente_repo.get_by_filters(
            entrenador_id=entrenador_id,
            cliente_id=cliente_id,
            activo=True
        )
        
        if not relaciones:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relación no encontrada"
            )
        
        # Desactivar relación
        self.entrenador_cliente_repo.update(relaciones[0].id, {
            "activo": False,
            "fecha_finalizacion": date.today()
        })
        
        return True
    
    # ========================================
    # ESTADÍSTICAS Y REPORTES
    # ========================================
    
    def get_estadisticas(self, entrenador_id: int) -> dict:
        """
        Obtiene estadísticas generales del entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Diccionario con estadísticas
        """
        clientes = self.get_mis_clientes(entrenador_id)
        rutinas = self.rutina_repo.get_by_creador(entrenador_id)
        dietas = self.dieta_repo.get_by_entrenador(entrenador_id)
        clases = self.clase_repo.get_by_entrenador(entrenador_id)
        
        return {
            "total_clientes": len(clientes),
            "clientes_activos": len([c for c in clientes if c.activo]),
            "total_rutinas_creadas": len(rutinas),
            "rutinas_activas": len([r for r in rutinas if r.activo]),
            "total_dietas_creadas": len(dietas),
            "dietas_activas": len([d for d in dietas if d.activo]),
            "total_clases": len(clases),
            "clases_activas": len([c for c in clases if c.activo])
        }
    
    def get_clientes_sin_rutina(self, entrenador_id: int) -> List[Usuario]:
        """
        Obtiene clientes que no tienen rutina asignada.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Lista de clientes sin rutina
        """
        clientes = self.get_mis_clientes(entrenador_id)
        clientes_sin_rutina = []
        
        for cliente in clientes:
            rutinas = self.rutina_repo.get_by_cliente(cliente.id)
            if not rutinas or not any(r.activo for r in rutinas):
                clientes_sin_rutina.append(cliente)
        
        return clientes_sin_rutina
    
    def get_clientes_sin_dieta(self, entrenador_id: int) -> List[Usuario]:
        """
        Obtiene clientes que no tienen dieta asignada.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Lista de clientes sin dieta
        """
        clientes = self.get_mis_clientes(entrenador_id)
        clientes_sin_dieta = []
        
        for cliente in clientes:
            dietas = self.dieta_repo.get_by_cliente(cliente.id)
            if not dietas or not any(d.activo for d in dietas):
                clientes_sin_dieta.append(cliente)
        
        return clientes_sin_dieta
    
    # ========================================
    # GESTIÓN DE CONTENIDO
    # ========================================
    
    def get_mis_rutinas(self, entrenador_id: int) -> List:
        """
        Obtiene todas las rutinas creadas por el entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Lista de rutinas
        """
        return self.rutina_repo.get_by_creador(entrenador_id)
    
    def get_mis_dietas(self, entrenador_id: int) -> List:
        """
        Obtiene todas las dietas creadas por el entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Lista de dietas
        """
        return self.dieta_repo.get_by_entrenador(entrenador_id)
    
    def get_mis_clases(self, entrenador_id: int) -> List:
        """
        Obtiene todas las clases del entrenador.
        
        Args:
            entrenador_id: ID del entrenador
            
        Returns:
            Lista de clases
        """
        return self.clase_repo.get_by_entrenador(entrenador_id)
    
    # ========================================
    # VALIDACIONES
    # ========================================
    
    def puede_editar_rutina(self, entrenador_id: int, rutina_id: int) -> bool:
        """
        Verifica si el entrenador puede editar una rutina.
        
        Args:
            entrenador_id: ID del entrenador
            rutina_id: ID de la rutina
            
        Returns:
            True si puede editar
        """
        rutina = self.rutina_repo.get_by_id(rutina_id)
        if not rutina:
            return False
        
        return rutina.creador_id == entrenador_id
    
    def puede_editar_dieta(self, entrenador_id: int, dieta_id: int) -> bool:
        """
        Verifica si el entrenador puede editar una dieta.
        
        Args:
            entrenador_id: ID del entrenador
            dieta_id: ID de la dieta
            
        Returns:
            True si puede editar
        """
        dieta = self.dieta_repo.get_by_id(dieta_id)
        if not dieta:
            return False
        
        return dieta.entrenador_id == entrenador_id