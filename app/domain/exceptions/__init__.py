"""Domain Exceptions"""
from app.domain.exceptions.base import DomainException
from app.domain.exceptions.auth_exception import (
    AuthenticationException,
    InvalidCredentialsException,
    TokenExpiredException,
    UnauthorizedException
)
from app.domain.exceptions.usuario_exceptions import (
    UsuarioNotFoundException,
    UsuarioInactivoException,
    EmailDuplicadoException
)
from app.domain.exceptions.gimnasio_exceptions import (
    GimnasioNotFoundException,
    GimnasioInactivoException,
    CodigoGimnasioDuplicadoException
)
from app.domain.exceptions.membresia_exceptions import (
    MembresiaNotFoundException,
    MembresiaVencidaException,
    MembresiaDuplicadaException
)
from app.domain.exceptions.validation_exceptions import (
    ValidationException,
    InvalidDataException,
    RequiredFieldException
)

__all__ = [
    # Base
    "DomainException",
    # Auth
    "AuthenticationException",
    "InvalidCredentialsException",
    "TokenExpiredException",
    "UnauthorizedException",
    # Usuario
    "UsuarioNotFoundException",
    "UsuarioInactivoException",
    "EmailDuplicadoException",
    # Gimnasio
    "GimnasioNotFoundException",
    "GimnasioInactivoException",
    "CodigoGimnasioDuplicadoException",
    # Membresía
    "MembresiaNotFoundException",
    "MembresiaVencidaException",
    "MembresiaDuplicadaException",
    # Validation
    "ValidationException",
    "InvalidDataException",
    "RequiredFieldException",
]