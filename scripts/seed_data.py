"""Script para poblar la base de datos con datos de prueba"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from datetime import date, datetime, timedelta
from decimal import Decimal

from app.core.database import SessionLocal
from app.services.gimnasio_service import GimnasioService
from app.services.rol_service import RolService
from app.services.usuario_service import UsuarioService
from app.services.membresia_service import MembresiaService
from app.services.membresia_tipo_service import MembresiaTipoService
from app.schemas.gimnasio import GimnasioCreate
from app.schemas.rol import RolCreate
from app.schemas.usuario import UsuarioCreate
from app.schemas.membresia import MembresiaCreate
from app.schemas.membresia_tipo import MembresiaTipoCreate

def seed_data():
    """Pobla la base de datos con datos de prueba"""
    db = SessionLocal()
    
    try:
        print("🌱 Sembrando datos de prueba...")
        
        # 1. Crear Gimnasio
        print("\n📍 Creando gimnasio...")
        gimnasio_service = GimnasioService(db)
        gimnasio = gimnasio_service.create(GimnasioCreate(
            nombre="Gym Pro",
            codigo_unico="GYMPRO2024",
            email="admin@gympro.com",
            telefono="5555551234",
            direccion="Av. Principal 123, Ciudad",
            activo=True
        ))
        print(f"   ✅ Gimnasio creado: {gimnasio.nombre} (ID: {gimnasio.id})")
        
        # 2. Crear Roles
        print("\n👥 Creando roles...")
        rol_service = RolService(db)
        
        roles = [
            {"nombre": "Admin", "descripcion": "Administrador del gimnasio"},
            {"nombre": "Entrenador", "descripcion": "Entrenador personal"},
            {"nombre": "Cliente", "descripcion": "Cliente del gimnasio"},
        ]
        
        roles_creados = []
        for rol_data in roles:
            rol = rol_service.create(RolCreate(**rol_data))
            roles_creados.append(rol)
            print(f"   ✅ Rol creado: {rol.nombre} (ID: {rol.id})")
        
        # 3. Crear Tipos de Membresía
        print("\n💳 Creando tipos de membresía...")
        membresia_tipo_service = MembresiaTipoService(db)
        
        tipos_membresia = [
            {
                "nombre": "Mensual",
                "duracion_dias": 30,
                "precio": Decimal("500.00"),
                "gimnasio_id": gimnasio.id,
                "descripcion": "Acceso por 1 mes"
            },
            {
                "nombre": "Trimestral",
                "duracion_dias": 90,
                "precio": Decimal("1350.00"),
                "gimnasio_id": gimnasio.id,
                "descripcion": "Acceso por 3 meses (10% descuento)"
            },
            {
                "nombre": "Anual",
                "duracion_dias": 365,
                "precio": Decimal("4800.00"),
                "gimnasio_id": gimnasio.id,
                "descripcion": "Acceso por 1 año (20% descuento)"
            },
        ]
        
        tipos_creados = []
        for tipo_data in tipos_membresia:
            tipo = membresia_tipo_service.create(MembresiaTipoCreate(**tipo_data))
            tipos_creados.append(tipo)
            print(f"   ✅ Tipo de membresía creado: {tipo.nombre} (${tipo.precio})")
        
        # 4. Crear Usuarios
        print("\n👤 Creando usuarios...")
        usuario_service = UsuarioService(db)
        
        # Admin
        admin = usuario_service.create(UsuarioCreate(
            nombre="Admin",
            apellido="Principal",
            email="admin@gympro.com",
            password="Admin123!",
            telefono="5555551234",
            gimnasio_id=gimnasio.id,
            rol_id=roles_creados[0].id,  # Admin
            fecha_nacimiento=date(1985, 1, 1),
            activo=True
        ))
        print(f"   ✅ Admin creado: {admin.email}")
        
        # Entrenador
        entrenador = usuario_service.create(UsuarioCreate(
            nombre="Carlos",
            apellido="Entrenador",
            email="carlos@gympro.com",
            password="Carlos123!",
            telefono="5555552345",
            gimnasio_id=gimnasio.id,
            rol_id=roles_creados[1].id,  # Entrenador
            fecha_nacimiento=date(1990, 5, 15),
            activo=True
        ))
        print(f"   ✅ Entrenador creado: {entrenador.email}")
        
        # Clientes
        clientes_data = [
            {
                "nombre": "Juan",
                "apellido": "Pérez",
                "email": "juan@example.com",
                "password": "Juan123!",
                "telefono": "5555553456",
                "fecha_nacimiento": date(1995, 3, 20)
            },
            {
                "nombre": "María",
                "apellido": "García",
                "email": "maria@example.com",
                "password": "Maria123!",
                "telefono": "5555554567",
                "fecha_nacimiento": date(1992, 7, 10)
            },
            {
                "nombre": "Pedro",
                "apellido": "López",
                "email": "pedro@example.com",
                "password": "Pedro123!",
                "telefono": "5555555678",
                "fecha_nacimiento": date(1988, 11, 25)
            },
        ]
        
        clientes = []
        for cliente_data in clientes_data:
            cliente = usuario_service.create(UsuarioCreate(
                **cliente_data,
                gimnasio_id=gimnasio.id,
                rol_id=roles_creados[2].id,  # Cliente
                activo=True
            ))
            clientes.append(cliente)
            print(f"   ✅ Cliente creado: {cliente.email}")
        
        # 5. Crear Membresías para clientes
        print("\n💳 Creando membresías...")
        membresia_service = MembresiaService(db)
        
        for i, cliente in enumerate(clientes):
            tipo = tipos_creados[i % len(tipos_creados)]
            fecha_inicio = date.today() - timedelta(days=i*5)
            fecha_fin = fecha_inicio + timedelta(days=tipo.duracion_dias)
            
            membresia = membresia_service.create(MembresiaCreate(
                usuario_id=cliente.id,
                membresia_tipo_id=tipo.id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                precio_pagado=tipo.precio
            ))
            print(f"   ✅ Membresía creada para {cliente.nombre}: {tipo.nombre}")
        
        print("\n✅ Datos de prueba creados exitosamente!")
        print("\n📝 Credenciales de acceso:")
        print("   Admin: admin@gympro.com / Admin123!")
        print("   Entrenador: carlos@gympro.com / Carlos123!")
        print("   Cliente: juan@example.com / Juan123!")
        
    except Exception as e:
        print(f"\n❌ Error al sembrar datos: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()