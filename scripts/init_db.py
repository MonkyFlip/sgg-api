"""Script para inicializar la base de datos"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.core.database import engine, Base
from app.models import *  # Importar todos los modelos

def init_db():
    """Inicializa la base de datos creando todas las tablas"""
    print("🔨 Creando tablas en la base de datos...")
    
    try:
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos inicializada correctamente")
        print(f"📊 Tablas creadas: {len(Base.metadata.tables)}")
        
        # Listar tablas creadas
        print("\n📋 Tablas:")
        for table_name in sorted(Base.metadata.tables.keys()):
            print(f"   - {table_name}")
            
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        sys.exit(1)

def drop_all_tables():
    """Elimina todas las tablas (usar con precaución)"""
    print("⚠️  ADVERTENCIA: Se eliminarán todas las tablas")
    confirm = input("¿Estás seguro? (escribir 'SI' para confirmar): ")
    
    if confirm == "SI":
        print("🗑️  Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tablas eliminadas")
    else:
        print("❌ Operación cancelada")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Inicializar base de datos")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Eliminar todas las tablas antes de crear"
    )
    
    args = parser.parse_args()
    
    if args.drop:
        drop_all_tables()
    
    init_db()