"""Validadores de datos"""
import re
from typing import Optional, Tuple

class Validator:
    """Clase con métodos de validación estáticos"""
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato de email"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, email))
    
    @staticmethod
    def validar_telefono(telefono: str, pais: str = "MX") -> bool:
        """
        Valida número de teléfono.
        
        Args:
            telefono: Número a validar
            pais: Código de país (MX, CL, AR, etc.)
        """
        # Eliminar espacios y caracteres especiales
        telefono_limpio = re.sub(r'[^\d]', '', telefono)
        
        if pais == "MX":
            return len(telefono_limpio) == 10
        elif pais == "CL":
            return len(telefono_limpio) == 9
        elif pais == "AR":
            return 10 <= len(telefono_limpio) <= 11
        else:
            return 7 <= len(telefono_limpio) <= 15
    
    @staticmethod
    def validar_rut(rut: str) -> bool:
        """
        Valida RUT chileno.
        
        Args:
            rut: RUT a validar (formato: 12345678-9)
        """
        # Limpiar RUT
        rut = rut.replace(".", "").replace("-", "").upper()
        
        if len(rut) < 2:
            return False
        
        cuerpo = rut[:-1]
        dv = rut[-1]
        
        # Calcular dígito verificador
        suma = 0
        multiplo = 2
        
        for i in reversed(cuerpo):
            suma += int(i) * multiplo
            multiplo = 2 if multiplo == 7 else multiplo + 1
        
        dv_calculado = 11 - (suma % 11)
        
        if dv_calculado == 11:
            dv_esperado = '0'
        elif dv_calculado == 10:
            dv_esperado = 'K'
        else:
            dv_esperado = str(dv_calculado)
        
        return dv == dv_esperado
    
    @staticmethod
    def validar_password_fuerte(password: str) -> Tuple[bool, str]:
        """
        Valida que una contraseña sea fuerte.
        
        Returns:
            (es_valida, mensaje_error)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "Debe contener al menos una mayúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "Debe contener al menos una minúscula"
        
        if not re.search(r'\d', password):
            return False, "Debe contener al menos un número"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Debe contener al menos un carácter especial"
        
        return True, "Contraseña válida"
    
    @staticmethod
    def validar_url(url: str) -> bool:
        """Valida una URL"""
        patron = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        return bool(re.match(patron, url))
    
    @staticmethod
    def validar_longitud(
        texto: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None
    ) -> bool:
        """Valida la longitud de un texto"""
        longitud = len(texto)
        
        if min_length and longitud < min_length:
            return False
        
        if max_length and longitud > max_length:
            return False
        
        return True
    
    @staticmethod
    def validar_rango(
        valor: float,
        min_valor: Optional[float] = None,
        max_valor: Optional[float] = None
    ) -> bool:
        """Valida que un valor esté en un rango"""
        if min_valor is not None and valor < min_valor:
            return False
        
        if max_valor is not None and valor > max_valor:
            return False
        
        return True

# Funciones helper para usar sin instanciar la clase
def validar_email(email: str) -> bool:
    """Valida email (función helper)"""
    return Validator.validar_email(email)

def validar_telefono(telefono: str, pais: str = "MX") -> bool:
    """Valida teléfono (función helper)"""
    return Validator.validar_telefono(telefono, pais)

def validar_rut(rut: str) -> bool:
    """Valida RUT chileno (función helper)"""
    return Validator.validar_rut(rut)

def validar_password_fuerte(password: str) -> Tuple[bool, str]:
    """Valida contraseña fuerte (función helper)"""
    return Validator.validar_password_fuerte(password)