"""Helper para generar y aplicar migraciones con Alembic"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import subprocess
from datetime import datetime

def create_migration(message: str):
    """
    Genera una nueva migración.
    
    Args:
        message: Descripción de los cambios
    """
    print(f"📝 Generando migración: {message}")
    
    try:
        subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", message],
            check=True
        )
        print("✅ Migración generada exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al generar migración: {e}")
        sys.exit(1)

def apply_migrations():
    """Aplica todas las migraciones pendientes"""
    print("🔄 Aplicando migraciones...")
    
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migraciones aplicadas exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al aplicar migraciones: {e}")
        sys.exit(1)

def rollback_migration(steps: int = 1):
    """
    Revierte migraciones.
    
    Args:
        steps: Número de pasos a revertir
    """
    print(f"⏮️  Revirtiendo {steps} migración(es)...")
    
    revision = f"-{steps}"
    
    try:
        subprocess.run(["alembic", "downgrade", revision], check=True)
        print("✅ Migración revertida exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al revertir migración: {e}")
        sys.exit(1)

def show_current_revision():
    """Muestra la revisión actual de la base de datos"""
    try:
        subprocess.run(["alembic", "current"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def show_history():
    """Muestra el historial de migraciones"""
    try:
        subprocess.run(["alembic", "history", "--verbose"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Helper para migraciones")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # Crear migración
    create_parser = subparsers.add_parser("create", help="Crear nueva migración")
    create_parser.add_argument("message", help="Mensaje de la migración")
    
    # Aplicar migraciones
    subparsers.add_parser("upgrade", help="Aplicar migraciones")
    
    # Revertir migración
    rollback_parser = subparsers.add_parser("downgrade", help="Revertir migración")
    rollback_parser.add_argument(
        "--steps",
        type=int,
        default=1,
        help="Número de pasos a revertir"
    )
    
    # Mostrar revisión actual
    subparsers.add_parser("current", help="Mostrar revisión actual")
    
    # Mostrar historial
    subparsers.add_parser("history", help="Mostrar historial de migraciones")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_migration(args.message)
    elif args.command == "upgrade":
        apply_migrations()
    elif args.command == "downgrade":
        rollback_migration(args.steps)
    elif args.command == "current":
        show_current_revision()
    elif args.command == "history":
        show_history()
    else:
        parser.print_help()