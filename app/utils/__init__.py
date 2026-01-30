"""
Utils module - Utilidades y helpers
"""

from app.utils.date_utils import (
    get_fecha_inicio_mes,
    get_fecha_fin_mes,
    calcular_edad,
    es_mayor_edad,
    dias_entre_fechas,
    fecha_hace_dias,
    formato_fecha_legible
)

from app.utils.email_utils import (
    validar_email,
    enviar_email,
    enviar_email_bienvenida,
    enviar_email_recuperacion,
    enviar_email_membresia_vencida
)

from app.utils.file_handler import (
    FileHandler,
    guardar_archivo,
    eliminar_archivo,
    validar_archivo,
    obtener_url_archivo
)

from app.utils.pagination import (
    Paginator,
    paginar,
    PaginationParams
)

from app.utils.pdf_generator import (
    PDFGenerator,
    generar_pdf_factura,
    generar_pdf_membresia,
    generar_pdf_reporte
)

from app.utils.validator import (
    Validator,
    validar_telefono,
    validar_email as validar_email_formato,
    validar_password_fuerte,
    validar_rut
)

__all__ = [
    # Date utils
    "get_fecha_inicio_mes",
    "get_fecha_fin_mes",
    "calcular_edad",
    "es_mayor_edad",
    "dias_entre_fechas",
    "fecha_hace_dias",
    "formato_fecha_legible",
    # Email utils
    "validar_email",
    "enviar_email",
    "enviar_email_bienvenida",
    "enviar_email_recuperacion",
    "enviar_email_membresia_vencida",
    # File handler
    "FileHandler",
    "guardar_archivo",
    "eliminar_archivo",
    "validar_archivo",
    "obtener_url_archivo",
    # Pagination
    "Paginator",
    "paginar",
    "PaginationParams",
    # PDF Generator
    "PDFGenerator",
    "generar_pdf_factura",
    "generar_pdf_membresia",
    "generar_pdf_reporte",
    # Validator
    "Validator",
    "validar_telefono",
    "validar_email_formato",
    "validar_password_fuerte",
    "validar_rut",
]