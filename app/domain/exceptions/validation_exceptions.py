"""Excepciones de Validación"""
from app.domain.exceptions.base import DomainException

class ValidationException(DomainException):
    """Excepción base de validación"""
    
    def __init__(self, message: str, campo: str = None, details: dict = None):
        if details is None:
            details = {}
        if campo:
            details["campo"] = campo
        
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=details
        )

class InvalidDataException(ValidationException):
    """Excepción cuando los datos son inválidos"""
    
    def __init__(self, campo: str, razon: str):
        super().__init__(
            message=f"Dato inválido en '{campo}': {razon}",
            campo=campo,
            details={"razon": razon}
        )

class RequiredFieldException(ValidationException):
    """Excepción cuando falta un campo requerido"""
    
    def __init__(self, campo: str):
        super().__init__(
            message=f"El campo '{campo}' es requerido",
            campo=campo
        )

class FormatoInvalidoException(ValidationException):
    """Excepción cuando el formato es inválido"""
    
    def __init__(self, campo: str, formato_esperado: str):
        super().__init__(
            message=f"Formato inválido en '{campo}'. Se esperaba: {formato_esperado}",
            campo=campo,
            details={"formato_esperado": formato_esperado}
        )

class RangoInvalidoException(ValidationException):
    """Excepción cuando un valor está fuera de rango"""
    
    def __init__(self, campo: str, min_valor: any, max_valor: any, valor_actual: any):
        super().__init__(
            message=f"Valor de '{campo}' fuera de rango. Debe estar entre {min_valor} y {max_valor}",
            campo=campo,
            details={
                "min": min_valor,
                "max": max_valor,
                "valor_actual": valor_actual
            }
        )