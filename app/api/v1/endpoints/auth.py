"""Endpoints de Autenticación"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.services.auth_service import AuthService
from app.schemas.auth import Login, Register, Token, PasswordChange
from app.schemas.usuario import UsuarioResponse

router = APIRouter()

@router.post("/login", response_model=Token)
def login(login_data: Login, db: Session = Depends(get_db)):
    """Login de usuario"""
    auth_service = AuthService(db)
    return auth_service.login(login_data)

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(register_data: Register, db: Session = Depends(get_db)):
    """Registro de nuevo usuario"""
    auth_service = AuthService(db)
    return auth_service.register(register_data)

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Renueva el access token"""
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(refresh_token)

@router.post("/change-password")
def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cambia la contraseña"""
    auth_service = AuthService(db)
    auth_service.change_password(
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )
    return {"message": "Contraseña actualizada exitosamente"}

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Info del usuario autenticado"""
    return current_user