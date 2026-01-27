"""
Módulo de Seguridad
Maneja autenticación, autorización, JWT tokens y hashing de passwords
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ============================================
# CONFIGURACIÓN DE PASSWORD HASHING
# ============================================

# Context para hashing de passwords con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================
# FUNCIONES DE PASSWORD
# ============================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña plana coincide con su hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña
        
    Returns:
        bool: True si coinciden, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro de una contraseña.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Valida la fortaleza de una contraseña.
    
    Requisitos:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    
    Args:
        password: Contraseña a validar
        
    Returns:
        tuple: (es_valida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not any(char.isupper() for char in password):
        return False, "La contraseña debe tener al menos una mayúscula"
    
    if not any(char.islower() for char in password):
        return False, "La contraseña debe tener al menos una minúscula"
    
    if not any(char.isdigit() for char in password):
        return False, "La contraseña debe tener al menos un número"
    
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_characters for char in password):
        return False, "La contraseña debe tener al menos un carácter especial"
    
    return True, "Contraseña válida"


# ============================================
# FUNCIONES DE JWT TOKEN
# ============================================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un token de acceso JWT.
    
    Args:
        data: Datos a incluir en el token (típicamente user_id, email, role, gimnasio_id)
        expires_delta: Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),  # Issued at
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crea un token de refresco JWT.
    
    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica y valida un token JWT.
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        dict: Payload del token si es válido, None si es inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verifica un token JWT y su tipo.
    
    Args:
        token: Token JWT a verificar
        token_type: Tipo de token esperado ('access' o 'refresh')
        
    Returns:
        dict: Payload del token si es válido, None si es inválido
    """
    payload = decode_token(token)
    
    if payload is None:
        return None
    
    # Verificar que el tipo de token sea el correcto
    if payload.get("type") != token_type:
        return None
    
    return payload


def extract_token_data(token: str) -> Optional[Dict[str, Any]]:
    """
    Extrae los datos del usuario del token.
    
    Args:
        token: Token JWT
        
    Returns:
        dict: Datos del usuario (user_id, email, role, gimnasio_id, etc.)
    """
    payload = decode_token(token)
    
    if payload is None:
        return None
    
    return {
        "user_id": payload.get("sub"),  # Subject (user_id)
        "email": payload.get("email"),
        "role": payload.get("role"),
        "gimnasio_id": payload.get("gimnasio_id"),
        "exp": payload.get("exp"),
        "iat": payload.get("iat"),
    }


def is_token_expired(token: str) -> bool:
    """
    Verifica si un token ha expirado.
    
    Args:
        token: Token JWT
        
    Returns:
        bool: True si expiró, False si aún es válido
    """
    payload = decode_token(token)
    
    if payload is None:
        return True
    
    exp_timestamp = payload.get("exp")
    if exp_timestamp is None:
        return True
    
    exp_datetime = datetime.fromtimestamp(exp_timestamp)
    return datetime.utcnow() > exp_datetime


# ============================================
# FUNCIONES DE AUTORIZACIÓN
# ============================================

def check_permission(
    user_role: str,
    required_roles: list[str]
) -> bool:
    """
    Verifica si un usuario tiene los permisos necesarios.
    
    Args:
        user_role: Rol del usuario
        required_roles: Lista de roles permitidos
        
    Returns:
        bool: True si tiene permiso, False en caso contrario
    """
    return user_role in required_roles


def is_super_admin(user_role: str) -> bool:
    """
    Verifica si un usuario es Super Admin.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si es Super Admin
    """
    return user_role == "super_admin"


def is_admin(user_role: str) -> bool:
    """
    Verifica si un usuario es Admin o Super Admin.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si es Admin o Super Admin
    """
    return user_role in ["super_admin", "admin"]


def is_entrenador(user_role: str) -> bool:
    """
    Verifica si un usuario es Entrenador.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si es Entrenador
    """
    return user_role == "entrenador"


def is_cliente(user_role: str) -> bool:
    """
    Verifica si un usuario es Cliente.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si es Cliente
    """
    return user_role == "cliente"


def can_manage_users(user_role: str) -> bool:
    """
    Verifica si un usuario puede gestionar otros usuarios.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si puede gestionar usuarios
    """
    return user_role in ["super_admin", "admin"]


def can_manage_gimnasio(user_role: str) -> bool:
    """
    Verifica si un usuario puede gestionar la configuración del gimnasio.
    
    Args:
        user_role: Rol del usuario
        
    Returns:
        bool: True si puede gestionar el gimnasio
    """
    return user_role == "super_admin"


# ============================================
# UTILIDADES DE SEGURIDAD
# ============================================

def generate_verification_code(length: int = 6) -> str:
    """
    Genera un código de verificación numérico.
    
    Args:
        length: Longitud del código
        
    Returns:
        str: Código de verificación
    """
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def generate_reset_token() -> str:
    """
    Genera un token seguro para reseteo de contraseña.
    
    Returns:
        str: Token de reseteo
    """
    import secrets
    return secrets.token_urlsafe(32)


def mask_email(email: str) -> str:
    """
    Enmascara un email para mostrarlo de forma segura.
    Ejemplo: juan.perez@gmail.com -> j***@gmail.com
    
    Args:
        email: Email a enmascarar
        
    Returns:
        str: Email enmascarado
    """
    if "@" not in email:
        return email
    
    username, domain = email.split("@")
    if len(username) <= 2:
        masked_username = username[0] + "*"
    else:
        masked_username = username[0] + "***"
    
    return f"{masked_username}@{domain}"


def mask_phone(phone: str) -> str:
    """
    Enmascara un número de teléfono.
    Ejemplo: +52 123 456 7890 -> +52 *** *** **90
    
    Args:
        phone: Teléfono a enmascarar
        
    Returns:
        str: Teléfono enmascarado
    """
    if len(phone) < 4:
        return phone
    
    return phone[:-2].replace(phone[2:-2], "*" * (len(phone) - 4)) + phone[-2:]