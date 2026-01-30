"""Generador de PDFs para reportes y documentos"""
from typing import Dict, List, Any
from datetime import datetime
from decimal import Decimal

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFGenerator:
    """Generador de PDFs para diversos documentos"""
    
    def __init__(self, filename: str, pagesize=letter):
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "reportlab no está instalado. Instala con: pip install reportlab"
            )
        
        self.filename = filename
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self.elements = []
    
    def add_title(self, text: str):
        """Agrega un título al PDF"""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        self.elements.append(Paragraph(text, title_style))
    
    def add_heading(self, text: str, level: int = 2):
        """Agrega un encabezado"""
        style = self.styles[f'Heading{level}']
        self.elements.append(Paragraph(text, style))
        self.elements.append(Spacer(1, 0.2*inch))
    
    def add_paragraph(self, text: str):
        """Agrega un párrafo"""
        self.elements.append(Paragraph(text, self.styles['Normal']))
        self.elements.append(Spacer(1, 0.1*inch))
    
    def add_table(self, data: List[List[Any]], col_widths: List[float] = None):
        """Agrega una tabla al PDF"""
        table = Table(data, colWidths=col_widths)
        
        # Estilo de tabla
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.3*inch))
    
    def add_spacer(self, height: float = 0.2):
        """Agrega espacio vertical"""
        self.elements.append(Spacer(1, height*inch))
    
    def build(self):
        """Construye el PDF"""
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=self.pagesize,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        doc.build(self.elements)
        return self.filename

def generar_pdf_factura(factura_data: Dict[str, Any], filename: str) -> str:
    """
    Genera un PDF de factura.
    
    Args:
        factura_data: Datos de la factura
        filename: Nombre del archivo PDF
        
    Returns:
        Ruta del archivo generado
    """
    pdf = PDFGenerator(filename)
    
    # Título
    pdf.add_title(f"FACTURA {factura_data.get('numero_factura', 'N/A')}")
    pdf.add_spacer()
    
    # Información del gimnasio
    pdf.add_heading("Información del Gimnasio", 3)
    pdf.add_paragraph(f"<b>Gimnasio:</b> {factura_data.get('gimnasio_nombre', 'N/A')}")
    pdf.add_paragraph(f"<b>Dirección:</b> {factura_data.get('gimnasio_direccion', 'N/A')}")
    pdf.add_spacer()
    
    # Información del cliente
    pdf.add_heading("Información del Cliente", 3)
    pdf.add_paragraph(f"<b>Cliente:</b> {factura_data.get('cliente_nombre', 'N/A')}")
    pdf.add_paragraph(f"<b>Email:</b> {factura_data.get('cliente_email', 'N/A')}")
    pdf.add_spacer()
    
    # Detalles de la factura
    pdf.add_heading("Detalles", 3)
    
    detalles = factura_data.get('detalles', [])
    if detalles:
        tabla_data = [['Descripción', 'Cantidad', 'Precio Unit.', 'Total']]
        
        for detalle in detalles:
            tabla_data.append([
                detalle.get('descripcion', ''),
                str(detalle.get('cantidad', 0)),
                f"${detalle.get('precio_unitario', 0):.2f}",
                f"${detalle.get('total', 0):.2f}"
            ])
        
        pdf.add_table(tabla_data, col_widths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    
    # Totales
    pdf.add_paragraph(f"<b>Subtotal:</b> ${factura_data.get('subtotal', 0):.2f}")
    pdf.add_paragraph(f"<b>Impuestos:</b> ${factura_data.get('impuestos', 0):.2f}")
    pdf.add_paragraph(f"<b>Descuentos:</b> ${factura_data.get('descuentos', 0):.2f}")
    pdf.add_paragraph(f"<b>TOTAL:</b> ${factura_data.get('total', 0):.2f}")
    
    return pdf.build()

def generar_pdf_membresia(membresia_data: Dict[str, Any], filename: str) -> str:
    """
    Genera un PDF de membresía.
    
    Args:
        membresia_data: Datos de la membresía
        filename: Nombre del archivo PDF
        
    Returns:
        Ruta del archivo generado
    """
    pdf = PDFGenerator(filename)
    
    # Título
    pdf.add_title("CERTIFICADO DE MEMBRESÍA")
    pdf.add_spacer()
    
    # Información
    pdf.add_paragraph(f"<b>Titular:</b> {membresia_data.get('titular', 'N/A')}")
    pdf.add_paragraph(f"<b>Tipo de Membresía:</b> {membresia_data.get('tipo', 'N/A')}")
    pdf.add_paragraph(f"<b>Fecha de Inicio:</b> {membresia_data.get('fecha_inicio', 'N/A')}")
    pdf.add_paragraph(f"<b>Fecha de Vencimiento:</b> {membresia_data.get('fecha_fin', 'N/A')}")
    pdf.add_paragraph(f"<b>Estado:</b> {membresia_data.get('estado', 'N/A')}")
    
    # Beneficios
    beneficios = membresia_data.get('beneficios', [])
    if beneficios:
        pdf.add_spacer()
        pdf.add_heading("Beneficios Incluidos", 3)
        for beneficio in beneficios:
            pdf.add_paragraph(f"• {beneficio}")
    
    return pdf.build()

def generar_pdf_reporte(
    titulo: str,
    datos: Dict[str, Any],
    tablas: List[Dict[str, Any]] = None,
    filename: str = "reporte.pdf"
) -> str:
    """
    Genera un PDF de reporte genérico.
    
    Args:
        titulo: Título del reporte
        datos: Datos del reporte
        tablas: Lista de tablas a incluir
        filename: Nombre del archivo PDF
        
    Returns:
        Ruta del archivo generado
    """
    pdf = PDFGenerator(filename)
    
    # Título
    pdf.add_title(titulo)
    pdf.add_paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    pdf.add_spacer()
    
    # Datos generales
    for key, value in datos.items():
        pdf.add_paragraph(f"<b>{key}:</b> {value}")
    
    # Tablas
    if tablas:
        for tabla_info in tablas:
            pdf.add_spacer()
            pdf.add_heading(tabla_info.get('titulo', 'Tabla'), 3)
            pdf.add_table(
                tabla_info.get('datos', []),
                tabla_info.get('col_widths', None)
            )
    
    return pdf.build()