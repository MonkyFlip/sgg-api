"""
Constantes globales de la aplicación SGG-API
"""

from enum import Enum


# ============================================
# ROLES DEL SISTEMA
# ============================================

class RolEnum(str, Enum):
    """Roles disponibles en el sistema"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    ENTRENADOR = "entrenador"
    CLIENTE = "cliente"


ROLES_ADMIN = [RolEnum.SUPER_ADMIN, RolEnum.ADMIN]
ROLES_STAFF = [RolEnum.SUPER_ADMIN, RolEnum.ADMIN, RolEnum.ENTRENADOR]
ROLES_ALL = [RolEnum.SUPER_ADMIN, RolEnum.ADMIN, RolEnum.ENTRENADOR, RolEnum.CLIENTE]


# ============================================
# ESTADOS DE MEMBRESÍA
# ============================================

class EstadoMembresiaEnum(str, Enum):
    """Estados posibles de una membresía"""
    ACTIVA = "activa"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"
    SUSPENDIDA = "suspendida"


# ============================================
# ESTADOS DE FACTURA
# ============================================

class EstadoFacturaEnum(str, Enum):
    """Estados posibles de una factura"""
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    CANCELADA = "cancelada"
    ANULADA = "anulada"


# ============================================
# MÉTODOS DE PAGO
# ============================================

class MetodoPagoEnum(str, Enum):
    """Métodos de pago disponibles"""
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"
    OTRO = "otro"


# ============================================
# TIPOS DE FACTURA
# ============================================

class TipoFacturaEnum(str, Enum):
    """Tipos de factura"""
    MEMBRESIA = "membresia"
    PRODUCTO = "producto"
    MIXTA = "mixta"


# ============================================
# TIPOS DE ITEM EN FACTURA
# ============================================

class TipoItemFacturaEnum(str, Enum):
    """Tipos de items en una factura"""
    MEMBRESIA = "membresia"
    PRODUCTO = "producto"


# ============================================
# GÉNERO
# ============================================

class GeneroEnum(str, Enum):
    """Géneros disponibles"""
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"


# ============================================
# DÍAS DE LA SEMANA
# ============================================

class DiaSemanaEnum(str, Enum):
    """Días de la semana"""
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"
    SABADO = "sabado"
    DOMINGO = "domingo"


DIAS_LABORALES = [
    DiaSemanaEnum.LUNES,
    DiaSemanaEnum.MARTES,
    DiaSemanaEnum.MIERCOLES,
    DiaSemanaEnum.JUEVES,
    DiaSemanaEnum.VIERNES
]

DIAS_FIN_SEMANA = [
    DiaSemanaEnum.SABADO,
    DiaSemanaEnum.DOMINGO
]


# ============================================
# TIPOS DE ACCESO
# ============================================

class TipoAccesoEnum(str, Enum):
    """Tipos de registro de acceso"""
    ENTRADA = "entrada"
    SALIDA = "salida"


# ============================================
# ESTADOS DE RESERVA
# ============================================

class EstadoReservaEnum(str, Enum):
    """Estados posibles de una reserva"""
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    ASISTIO = "asistio"
    NO_ASISTIO = "no_asistio"


# ============================================
# ESTADOS DE EQUIPAMIENTO
# ============================================

class EstadoEquipamientoEnum(str, Enum):
    """Estados del equipamiento del gimnasio"""
    EXCELENTE = "excelente"
    BUENO = "bueno"
    REGULAR = "regular"
    MALO = "malo"
    FUERA_SERVICIO = "fuera_servicio"


# ============================================
# NIVEL DE ENTRENAMIENTO
# ============================================

class NivelEntrenamientoEnum(str, Enum):
    """Niveles de entrenamiento"""
    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZADO = "avanzado"


# ============================================
# TIPO DE RUTINA
# ============================================

class TipoRutinaEnum(str, Enum):
    """Tipos de rutina"""
    GENERAL = "general"
    PERSONALIZADA = "personalizada"


# ============================================
# TIPO DE COMIDA
# ============================================

class TipoComidaEnum(str, Enum):
    """Tipos de comida en un plan alimenticio"""
    DESAYUNO = "desayuno"
    COLACION_AM = "colacion_am"
    ALMUERZO = "almuerzo"
    COLACION_PM = "colacion_pm"
    CENA = "cena"
    COLACION_NOCHE = "colacion_noche"


# ============================================
# TIPO DE NOTIFICACIÓN
# ============================================

class TipoNotificacionEnum(str, Enum):
    """Tipos de notificación"""
    INFORMACION = "informacion"
    RECORDATORIO = "recordatorio"
    ALERTA = "alerta"
    PROMOCION = "promocion"


# ============================================
# MENSAJES DE ERROR COMUNES
# ============================================

ERROR_MESSAGES = {
    # Autenticación
    "AUTH_INVALID_CREDENTIALS": "Credenciales inválidas",
    "AUTH_USER_NOT_FOUND": "Usuario no encontrado",
    "AUTH_USER_INACTIVE": "Usuario inactivo",
    "AUTH_TOKEN_EXPIRED": "Token expirado",
    "AUTH_TOKEN_INVALID": "Token inválido",
    "AUTH_INSUFFICIENT_PERMISSIONS": "Permisos insuficientes",
    
    # Usuarios
    "USER_EMAIL_EXISTS": "El email ya está registrado",
    "USER_NOT_FOUND": "Usuario no encontrado",
    "USER_CANNOT_DELETE_SELF": "No puedes eliminar tu propia cuenta",
    
    # Gimnasios
    "GYM_NOT_FOUND": "Gimnasio no encontrado",
    "GYM_CODE_EXISTS": "El código de gimnasio ya existe",
    "GYM_UNAUTHORIZED": "No tienes acceso a este gimnasio",
    
    # Membresías
    "MEMBERSHIP_NOT_FOUND": "Membresía no encontrada",
    "MEMBERSHIP_EXPIRED": "Membresía expirada",
    "MEMBERSHIP_ALREADY_ACTIVE": "Ya tiene una membresía activa",
    
    # Accesos
    "ACCESS_MEMBERSHIP_REQUIRED": "Membresía activa requerida para acceder",
    "ACCESS_ALREADY_INSIDE": "El usuario ya registró entrada",
    "ACCESS_NOT_INSIDE": "El usuario no ha registrado entrada",
    
    # Clases
    "CLASS_NOT_FOUND": "Clase no encontrada",
    "CLASS_FULL": "La clase está llena",
    "CLASS_ALREADY_RESERVED": "Ya tienes una reserva para esta clase",
    
    # Productos
    "PRODUCT_NOT_FOUND": "Producto no encontrado",
    "PRODUCT_INSUFFICIENT_STOCK": "Stock insuficiente",
    
    # Facturas
    "INVOICE_NOT_FOUND": "Factura no encontrada",
    "INVOICE_ALREADY_PAID": "La factura ya está pagada",
    
    # Inventario
    "EQUIPMENT_NOT_FOUND": "Equipamiento no encontrado",
    
    # Rutinas
    "ROUTINE_NOT_FOUND": "Rutina no encontrada",
    "ROUTINE_NOT_ASSIGNED": "No tienes una rutina asignada",
    
    # Dietas
    "DIET_NOT_FOUND": "Dieta no encontrada",
    "DIET_NOT_ASSIGNED": "No tienes una dieta asignada",
    
    # Entrenadores
    "TRAINER_NOT_FOUND": "Entrenador no encontrado",
    "TRAINER_ALREADY_ASSIGNED": "El cliente ya tiene un entrenador asignado",
    "TRAINER_NOT_ASSIGNED": "El cliente no tiene entrenador asignado",
    
    # General
    "VALIDATION_ERROR": "Error de validación",
    "INTERNAL_ERROR": "Error interno del servidor",
    "NOT_FOUND": "Recurso no encontrado",
    "BAD_REQUEST": "Solicitud incorrecta",
}


# ============================================
# MENSAJES DE ÉXITO COMUNES
# ============================================

SUCCESS_MESSAGES = {
    # CRUD Genérico
    "CREATED": "Creado exitosamente",
    "UPDATED": "Actualizado exitosamente",
    "DELETED": "Eliminado exitosamente",
    
    # Autenticación
    "LOGIN_SUCCESS": "Inicio de sesión exitoso",
    "LOGOUT_SUCCESS": "Cierre de sesión exitoso",
    "PASSWORD_CHANGED": "Contraseña cambiada exitosamente",
    
    # Usuarios
    "USER_REGISTERED": "Usuario registrado exitosamente",
    "USER_ACTIVATED": "Usuario activado",
    "USER_DEACTIVATED": "Usuario desactivado",
    
    # Membresías
    "MEMBERSHIP_ACTIVATED": "Membresía activada",
    "MEMBERSHIP_RENEWED": "Membresía renovada",
    "MEMBERSHIP_CANCELLED": "Membresía cancelada",
    
    # Accesos
    "ACCESS_ENTRY_REGISTERED": "Entrada registrada",
    "ACCESS_EXIT_REGISTERED": "Salida registrada",
    
    # Reservas
    "RESERVATION_CREATED": "Reserva creada exitosamente",
    "RESERVATION_CANCELLED": "Reserva cancelada",
    
    # Pagos
    "PAYMENT_PROCESSED": "Pago procesado exitosamente",
    
    # Notificaciones
    "NOTIFICATION_SENT": "Notificación enviada",
}


# ============================================
# LÍMITES Y CONFIGURACIONES
# ============================================

# Límites de caracteres
MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 150
MAX_PASSWORD_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 1000
MAX_PHONE_LENGTH = 20

# Configuraciones de membresía
MIN_MEMBERSHIP_DAYS = 1
MAX_MEMBERSHIP_DAYS = 365 * 2  # 2 años

# Configuraciones de reservas
MAX_RESERVATIONS_PER_USER = 10
CANCELLATION_HOURS_BEFORE = 2  # Horas antes para cancelar

# Configuraciones de inventario
MIN_STOCK_ALERT = 5

# Configuraciones de rutinas
MAX_EXERCISES_PER_DAY = 20
MIN_SERIES = 1
MAX_SERIES = 10

# Configuraciones de dietas
MAX_MEALS_PER_DAY = 8
MIN_CALORIES = 800
MAX_CALORIES = 5000


# ============================================
# EXPRESIONES REGULARES
# ============================================

# Validación de email
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Validación de teléfono (formato internacional)
PHONE_REGEX = r'^\+?[1-9]\d{1,14}$'

# Validación de código postal (México)
POSTAL_CODE_MX_REGEX = r'^\d{5}$'


# ============================================
# FORMATOS DE FECHA
# ============================================

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"
DISPLAY_DATETIME_FORMAT = "%d/%m/%Y %H:%M"


# ============================================
# CÓDIGOS HTTP PERSONALIZADOS
# ============================================

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500


# ============================================
# TAGS PARA DOCUMENTACIÓN DE API
# ============================================

API_TAGS = {
    "auth": "Autenticación",
    "gimnasios": "Gimnasios",
    "usuarios": "Usuarios",
    "roles": "Roles",
    "membresias": "Membresías",
    "accesos": "Control de Acceso",
    "entrenadores": "Entrenadores",
    "clases": "Clases Grupales",
    "reservas": "Reservas",
    "productos": "Productos",
    "facturas": "Facturación",
    "pagos": "Pagos",
    "inventario": "Inventario",
    "rutinas": "Rutinas",
    "dietas": "Dietas",
    "progreso": "Progreso Físico",
    "notificaciones": "Notificaciones",
    "reportes": "Reportes y Estadísticas",
}