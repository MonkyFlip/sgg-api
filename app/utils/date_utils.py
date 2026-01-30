"""Utilidades para manejo de fechas"""
from datetime import date, datetime, timedelta
from calendar import monthrange
from typing import Optional

def get_fecha_inicio_mes(fecha: date = None) -> date:
    """Obtiene el primer día del mes"""
    if fecha is None:
        fecha = date.today()
    return date(fecha.year, fecha.month, 1)

def get_fecha_fin_mes(fecha: date = None) -> date:
    """Obtiene el último día del mes"""
    if fecha is None:
        fecha = date.today()
    ultimo_dia = monthrange(fecha.year, fecha.month)[1]
    return date(fecha.year, fecha.month, ultimo_dia)

def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula la edad de una persona"""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

def es_mayor_edad(fecha_nacimiento: date, edad_minima: int = 18) -> bool:
    """Verifica si una persona es mayor de edad"""
    return calcular_edad(fecha_nacimiento) >= edad_minima

def dias_entre_fechas(fecha_inicio: date, fecha_fin: date) -> int:
    """Calcula días entre dos fechas"""
    return (fecha_fin - fecha_inicio).days

def fecha_hace_dias(dias: int) -> date:
    """Obtiene la fecha de hace N días"""
    return date.today() - timedelta(days=dias)

def formato_fecha_legible(fecha: date, incluir_hora: bool = False) -> str:
    """Formatea una fecha en formato legible"""
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    
    if isinstance(fecha, datetime):
        if incluir_hora:
            return f"{fecha.day} de {meses[fecha.month-1]} de {fecha.year} a las {fecha.strftime('%H:%M')}"
        fecha = fecha.date()
    
    return f"{fecha.day} de {meses[fecha.month-1]} de {fecha.year}"

def es_fin_semana(fecha: date = None) -> bool:
    """Verifica si una fecha es fin de semana"""
    if fecha is None:
        fecha = date.today()
    return fecha.weekday() >= 5

def agregar_dias_habiles(fecha: date, dias: int) -> date:
    """Agrega días hábiles a una fecha (excluye fines de semana)"""
    dias_agregados = 0
    fecha_actual = fecha
    
    while dias_agregados < dias:
        fecha_actual += timedelta(days=1)
        if not es_fin_semana(fecha_actual):
            dias_agregados += 1
    
    return fecha_actual