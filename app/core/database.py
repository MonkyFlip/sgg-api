"""
Configuración de la base de datos
Maneja la conexión a MySQL usando SQLAlchemy
"""

from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.core.config import settings

# ============================================
# CONFIGURACIÓN DEL ENGINE
# ============================================

# Crear engine de SQLAlchemy con pool de conexiones
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Mostrar queries SQL en logs (solo en desarrollo)
    poolclass=QueuePool,
    pool_size=settings.DB_POOL_SIZE,  # Número de conexiones en el pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Conexiones adicionales si el pool está lleno
    pool_timeout=settings.DB_POOL_TIMEOUT,  # Timeout en segundos para obtener conexión
    pool_recycle=settings.DB_POOL_RECYCLE,  # Reciclar conexiones después de X segundos
    pool_pre_ping=True,  # Verificar conexión antes de usarla
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
    }
)

# ============================================
# SESIÓN DE BASE DE DATOS
# ============================================

# Crear SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ============================================
# BASE DECLARATIVA
# ============================================

# Metadata con convención de nombres
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Base para todos los modelos
Base = declarative_base(metadata=metadata)


# ============================================
# DEPENDENCY INJECTION
# ============================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos.
    
    Uso en FastAPI:
    ```python
    @router.get("/usuarios")
    def get_usuarios(db: Session = Depends(get_db)):
        return db.query(Usuario).all()
    ```
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def init_db() -> None:
    """
    Inicializa la base de datos.
    Crea todas las tablas definidas en los modelos.
    
    IMPORTANTE: Solo usar en desarrollo.
    En producción usar Alembic para migraciones.
    """
    # Importar todos los modelos aquí para que SQLAlchemy los registre
    # from app.models import gimnasio, usuario, rol, etc...
    
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos inicializada correctamente")


def drop_db() -> None:
    """
    Elimina todas las tablas de la base de datos.
    
    ⚠️ PELIGRO: Solo usar en desarrollo/testing
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas han sido eliminadas")


def check_db_connection() -> bool:
    """
    Verifica la conexión a la base de datos.
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return False


# ============================================
# CONTEXT MANAGER PARA TRANSACCIONES
# ============================================

class DatabaseSession:
    """
    Context manager para manejar sesiones de base de datos.
    
    Uso:
    ```python
    with DatabaseSession() as db:
        usuario = db.query(Usuario).first()
        # La transacción se commitea automáticamente al salir del context
    ```
    """
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def __enter__(self) -> Session:
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Si hubo una excepción, hacer rollback
            self.db.rollback()
        else:
            # Si todo salió bien, hacer commit
            self.db.commit()
        
        self.db.close()


# ============================================
# FUNCIONES PARA TESTING
# ============================================

def get_test_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener una sesión de base de datos de prueba.
    Se usa en los tests para aislar cada test con una transacción.
    
    Yields:
        Session: Sesión de SQLAlchemy para testing
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ============================================
# INFORMACIÓN DE LA BASE DE DATOS
# ============================================

def get_db_info() -> dict:
    """
    Obtiene información sobre la base de datos actual.
    
    Returns:
        dict: Información de la base de datos
    """
    return {
        "host": settings.DB_HOST,
        "port": settings.DB_PORT,
        "database": settings.DB_NAME,
        "user": settings.DB_USER,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "echo": settings.DB_ECHO,
    }


def get_pool_status() -> dict:
    """
    Obtiene el estado actual del pool de conexiones.
    
    Returns:
        dict: Estado del pool de conexiones
    """
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "total": pool.size() + pool.overflow(),
    }


# ============================================
# VERIFICACIÓN INICIAL
# ============================================

# Verificar conexión al iniciar (opcional, comentar si no se desea)
if settings.DEBUG:
    check_db_connection()