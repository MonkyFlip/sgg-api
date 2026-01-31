"""
Configuración de la aplicación SGG-API
Maneja todas las variables de entorno y configuraciones globales
"""

from typing import List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator, model_validator
import secrets


class Settings(BaseSettings):
    """
    Configuración principal de la aplicación.
    Lee automáticamente las variables de entorno del archivo .env
    """
    
    # ============================================
    # APPLICATION
    # ============================================
    APP_NAME: str = "SGG-API"
    PROJECT_NAME: str = "SGG-API"  # Alias para compatibilidad
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Sistema Gestor de Gimnasios - API"
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # ============================================
    # SERVER
    # ============================================
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # ============================================
    # DATABASE
    # ============================================
    DATABASE_URL: Optional[str] = None  # Se puede pasar directamente en .env
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "sgg"
    DB_ECHO: bool = False
    
    # Database Connection Pool
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def build_database_url(cls, v, info):
        """Construye la URL de conexión a MySQL si no se proporciona"""
        if v:
            return v
        # Construir desde componentes individuales
        values = info.data
        user = values.get("DB_USER", "root")
        password = values.get("DB_PASSWORD", "")
        host = values.get("DB_HOST", "localhost")
        port = values.get("DB_PORT", 3306)
        db_name = values.get("DB_NAME", "sgg")
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"
    
    # ============================================
    # SECURITY
    # ============================================
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password Hashing
    BCRYPT_ROUNDS: int = 12
    
    @field_validator("SECRET_KEY", mode="after")
    @classmethod
    def validate_secret_key(cls, v):
        """Valida que la SECRET_KEY sea segura en producción"""
        if len(v) < 32:
            raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")
        return v
    
    # ============================================
    # CORS
    # ============================================
    # Usar Union para aceptar tanto string como lista
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:3000,http://localhost:3001"
    )
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:3000,http://localhost:3001"
    )
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    @field_validator("CORS_ORIGINS", "BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parsea los orígenes de CORS si vienen como string"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    # ============================================
    # FILE UPLOAD
    # ============================================
    MAX_FILE_SIZE: int = 10485760  # 10MB en bytes
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    ALLOWED_DOCUMENT_TYPES: List[str] = ["application/pdf"]
    UPLOAD_DIR: str = "./uploads"
    
    # ============================================
    # EMAIL CONFIGURATION
    # ============================================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    EMAIL_FROM: str = "noreply@sgg.com"
    EMAIL_FROM_NAME: str = "SGG Sistema"
    
    # ============================================
    # AWS S3 (Opcional)
    # ============================================
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    
    # ============================================
    # LOGGING
    # ============================================
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    LOG_FILE: str = "./logs/sgg-api.log"
    LOG_MAX_SIZE: int = 10485760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # ============================================
    # PAGINATION
    # ============================================
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    @field_validator("DEFAULT_PAGE_SIZE", mode="after")
    @classmethod
    def validate_page_size(cls, v, info):
        """Valida que el tamaño de página por defecto no exceda el máximo"""
        values = info.data
        max_size = values.get("MAX_PAGE_SIZE", 100)
        if v > max_size:
            raise ValueError(f"DEFAULT_PAGE_SIZE no puede ser mayor que MAX_PAGE_SIZE ({max_size})")
        return v
    
    # ============================================
    # RATE LIMITING
    # ============================================
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # ============================================
    # EXTERNAL SERVICES (Opcional)
    # ============================================
    # Payment Gateway
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    
    # SMS Service (Twilio)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # ============================================
    # MONITORING (Opcional)
    # ============================================
    SENTRY_DSN: Optional[str] = None
    
    # ============================================
    # CACHE (Redis - Opcional)
    # ============================================
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    CACHE_TTL: int = 300  # 5 minutos
    
    @property
    def REDIS_URL(self) -> str:
        """Construye la URL de conexión a Redis"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # ============================================
    # BACKUP
    # ============================================
    BACKUP_DIR: str = "./backups"
    AUTO_BACKUP_ENABLED: bool = True
    BACKUP_HOUR: int = 2  # 2 AM
    
    @field_validator("BACKUP_HOUR", mode="after")
    @classmethod
    def validate_backup_hour(cls, v):
        """Valida que la hora de backup esté entre 0 y 23"""
        if not 0 <= v <= 23:
            raise ValueError("BACKUP_HOUR debe estar entre 0 y 23")
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        arbitrary_types_allowed=True
    )


# Instancia global de configuración
settings = Settings()


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def get_settings() -> Settings:
    """
    Obtiene la instancia de configuración.
    Útil para dependency injection en FastAPI.
    """
    return settings


def is_production() -> bool:
    """Verifica si está en modo producción"""
    return settings.ENVIRONMENT == "production"


def is_development() -> bool:
    """Verifica si está en modo desarrollo"""
    return settings.ENVIRONMENT == "development"


def is_staging() -> bool:
    """Verifica si está en modo staging"""
    return settings.ENVIRONMENT == "staging"