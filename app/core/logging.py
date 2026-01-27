"""
Configuración del sistema de logging
Maneja los logs de la aplicación con rotación automática
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

from app.core.config import settings


# ============================================
# CONFIGURACIÓN DE FORMATO
# ============================================

# Formato detallado para archivos
DETAILED_FORMAT = (
    "[%(asctime)s] [%(levelname)s] [%(name)s] "
    "[%(filename)s:%(lineno)d] - %(message)s"
)

# Formato simple para consola
SIMPLE_FORMAT = "[%(levelname)s] %(name)s - %(message)s"

# Formato de fecha
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ============================================
# CONFIGURACIÓN DE NIVELES
# ============================================

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


# ============================================
# FUNCIONES DE CONFIGURACIÓN
# ============================================

def setup_logging() -> None:
    """
    Configura el sistema de logging de la aplicación.
    
    Crea:
    - Handler para archivo con rotación
    - Handler para consola
    - Formatters apropiados
    """
    
    # Crear directorio de logs si no existe
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Obtener el logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVELS.get(settings.LOG_LEVEL, logging.INFO))
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # ============================================
    # HANDLER PARA ARCHIVO (con rotación)
    # ============================================
    file_handler = RotatingFileHandler(
        filename=settings.LOG_FILE,
        maxBytes=settings.LOG_MAX_SIZE,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(LOG_LEVELS.get(settings.LOG_LEVEL, logging.INFO))
    file_formatter = logging.Formatter(DETAILED_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # ============================================
    # HANDLER PARA CONSOLA
    # ============================================
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVELS.get(settings.LOG_LEVEL, logging.INFO))
    console_formatter = logging.Formatter(SIMPLE_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # ============================================
    # CONFIGURAR LOGGERS DE LIBRERÍAS
    # ============================================
    
    # SQLAlchemy
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DB_ECHO else logging.WARNING
    )
    
    # Uvicorn
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    
    # FastAPI
    logging.getLogger("fastapi").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para un módulo específico.
    
    Args:
        name: Nombre del módulo (típicamente __name__)
        
    Returns:
        logging.Logger: Logger configurado
        
    Uso:
    ```python
    from app.core.logging import get_logger
    
    logger = get_logger(__name__)
    logger.info("Mensaje de información")
    logger.error("Mensaje de error")
    ```
    """
    return logging.getLogger(name)


# ============================================
# CLASE CUSTOMIZADA DE LOGGER
# ============================================

class CustomLogger:
    """
    Logger personalizado con métodos adicionales de conveniencia.
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log de nivel DEBUG"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log de nivel INFO"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log de nivel WARNING"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs) -> None:
        """Log de nivel ERROR"""
        self.logger.error(message, exc_info=exc_info, extra=kwargs)
    
    def critical(self, message: str, exc_info: bool = True, **kwargs) -> None:
        """Log de nivel CRITICAL"""
        self.logger.critical(message, exc_info=exc_info, extra=kwargs)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log de excepción con traceback completo"""
        self.logger.exception(message, extra=kwargs)
    
    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration: float,
        user_id: Optional[int] = None
    ) -> None:
        """
        Log específico para requests HTTP.
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Path del endpoint
            status_code: Código de estado HTTP
            duration: Duración en segundos
            user_id: ID del usuario que hizo el request (opcional)
        """
        self.info(
            f"{method} {path} - {status_code} - {duration:.3f}s",
            user_id=user_id,
            method=method,
            path=path,
            status_code=status_code,
            duration=duration
        )
    
    def log_db_query(
        self,
        query: str,
        duration: float,
        rows_affected: int = 0
    ) -> None:
        """
        Log específico para queries de base de datos.
        
        Args:
            query: Query SQL ejecutado
            duration: Duración en segundos
            rows_affected: Número de filas afectadas
        """
        self.debug(
            f"DB Query: {query[:100]}... - {duration:.3f}s - {rows_affected} rows",
            query=query,
            duration=duration,
            rows_affected=rows_affected
        )
    
    def log_auth_attempt(
        self,
        email: str,
        success: bool,
        ip_address: Optional[str] = None
    ) -> None:
        """
        Log específico para intentos de autenticación.
        
        Args:
            email: Email del usuario
            success: Si la autenticación fue exitosa
            ip_address: Dirección IP del intento
        """
        status = "SUCCESS" if success else "FAILED"
        self.info(
            f"Auth attempt - {email} - {status}",
            email=email,
            success=success,
            ip_address=ip_address
        )
    
    def log_business_event(
        self,
        event_type: str,
        entity: str,
        entity_id: int,
        action: str,
        user_id: Optional[int] = None,
        **kwargs
    ) -> None:
        """
        Log específico para eventos de negocio importantes.
        
        Args:
            event_type: Tipo de evento (CREATE, UPDATE, DELETE, etc.)
            entity: Entidad afectada (Usuario, Membresia, etc.)
            entity_id: ID de la entidad
            action: Descripción de la acción
            user_id: Usuario que ejecutó la acción
            **kwargs: Datos adicionales
        """
        self.info(
            f"Business Event - {event_type} - {entity}:{entity_id} - {action}",
            event_type=event_type,
            entity=entity,
            entity_id=entity_id,
            action=action,
            user_id=user_id,
            **kwargs
        )


# ============================================
# DECORADOR PARA LOGGING AUTOMÁTICO
# ============================================

def log_execution(logger: Optional[logging.Logger] = None):
    """
    Decorador para loggear la ejecución de funciones automáticamente.
    
    Uso:
    ```python
    @log_execution()
    def mi_funcion(param1, param2):
        return resultado
    ```
    """
    def decorator(func):
        from functools import wraps
        import time
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            logger.debug(f"Executing {func.__name__} with args={args}, kwargs={kwargs}")
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(f"Completed {func.__name__} in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    f"Error in {func.__name__} after {duration:.3f}s: {str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


# ============================================
# INICIALIZACIÓN
# ============================================

# Configurar logging al importar el módulo
setup_logging()

# Logger por defecto de la aplicación
app_logger = CustomLogger("sgg-api")