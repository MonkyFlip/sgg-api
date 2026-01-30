"""Schemas Base"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class ResponseBase(BaseModel):
    """Schema base para respuestas"""
    model_config = ConfigDict(from_attributes=True)

class PaginatedResponse(BaseModel, Generic[T]):
    """Schema para respuestas paginadas"""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int
    
    model_config = ConfigDict(from_attributes=True)