"""Service de Entrenador-Cliente"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.entrenador_cliente import EntrenadorClienteRepository
from app.schemas.entrenador_cliente import EntrenadorClienteCreate, EntrenadorClienteUpdate

class EntrenadorClienteService:
    def __init__(self, db: Session):
        self.repo = EntrenadorClienteRepository(db)
    
    def create(self, data: EntrenadorClienteCreate):
        if self.repo.existe_relacion(data.entrenador_id, data.cliente_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relación ya existe")
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación no encontrada")
        return obj
    
    def get_clientes_entrenador(self, entrenador_id: int):
        return self.repo.get_clientes_entrenador(entrenador_id)
    
    def update(self, id: int, data: EntrenadorClienteUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True