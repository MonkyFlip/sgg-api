"""Service de Reserva"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.reserva import ReservaRepository
from app.repositories.clase_horario import ClaseHorarioRepository
from app.schemas.reserva import ReservaCreate, ReservaUpdate

class ReservaService:
    def __init__(self, db: Session):
        self.repo = ReservaRepository(db)
        self.horario_repo = ClaseHorarioRepository(db)
    
    def create(self, data: ReservaCreate):
        # Verificar si ya tiene reserva
        if self.repo.tiene_reserva(data.usuario_id, data.clase_horario_id, data.fecha_reserva):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya tienes una reserva para esta clase")
        
        # Verificar capacidad (necesitaríamos obtener la clase desde horario)
        # count = self.repo.contar_reservas_horario(data.clase_horario_id, data.fecha_reserva)
        # if count >= clase.capacidad_maxima:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Clase llena")
        
        return self.repo.create(data.model_dump())
    
    def get_by_id(self, id: int):
        obj = self.repo.get_by_id(id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
        return obj
    
    def get_by_usuario(self, usuario_id: int):
        return self.repo.get_by_usuario(usuario_id)
    
    def update(self, id: int, data: ReservaUpdate):
        return self.repo.update(id, data.model_dump(exclude_unset=True))
    
    def delete(self, id: int):
        if not self.repo.delete(id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No encontrado")
        return True