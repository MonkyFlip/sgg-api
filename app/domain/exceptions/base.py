"""Excepción Base de Dominio"""

class DomainException(Exception):
    """
    Excepción base para todas las excepciones de dominio.
    
    Attributes:
        message: Mensaje de error
        code: Código de error único
        details: Detalles adicionales del error
    """
    
    def __init__(
        self,
        message: str,
        code: str = "DOMAIN_ERROR",
        details: dict = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convierte la excepción a diccionario"""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details
        }
    
    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code}, message={self.message})"