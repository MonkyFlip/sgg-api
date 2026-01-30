"""Utilidades para envío de emails"""
import re
from typing import List

def validar_email(email: str) -> bool:
    """Valida el formato de un email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))

def enviar_email(
    destinatario: str,
    asunto: str,
    cuerpo: str,
    html: bool = False,
    cc: List[str] = None,
    bcc: List[str] = None
) -> bool:
    """
    Envía un email.
    
    Note:
        Esta es una función de ejemplo. En producción, configurar
        con servicios como SendGrid, AWS SES, o SMTP real.
    """
    try:
        print(f"📧 Email enviado a {destinatario}: {asunto}")
        return True
    except Exception as e:
        print(f"❌ Error enviando email: {e}")
        return False

def enviar_email_bienvenida(destinatario: str, nombre: str, gimnasio: str) -> bool:
    """Envía email de bienvenida a un nuevo usuario"""
    asunto = f"¡Bienvenido a {gimnasio}!"
    
    cuerpo = f"""
    <html>
        <body>
            <h2>¡Hola {nombre}!</h2>
            <p>Te damos la bienvenida a <strong>{gimnasio}</strong>.</p>
            <p>Tu cuenta ha sido creada exitosamente.</p>
            <p>Ya puedes comenzar a disfrutar de nuestras instalaciones.</p>
            <br>
            <p>¡Nos vemos en el gym!</p>
            <p>Equipo de {gimnasio}</p>
        </body>
    </html>
    """
    
    return enviar_email(destinatario, asunto, cuerpo, html=True)

def enviar_email_recuperacion(destinatario: str, nombre: str, token: str) -> bool:
    """Envía email de recuperación de contraseña"""
    asunto = "Recuperación de contraseña"
    url_recuperacion = f"https://app.gimnasio.com/reset-password?token={token}"
    
    cuerpo = f"""
    <html>
        <body>
            <h2>Hola {nombre},</h2>
            <p>Recibimos una solicitud para restablecer tu contraseña.</p>
            <p>Haz clic en el siguiente enlace:</p>
            <p><a href="{url_recuperacion}">Restablecer contraseña</a></p>
            <p>Este enlace expirará en 24 horas.</p>
        </body>
    </html>
    """
    
    return enviar_email(destinatario, asunto, cuerpo, html=True)

def enviar_email_membresia_vencida(destinatario: str, nombre: str, fecha_vencimiento: str) -> bool:
    """Envía email notificando membresía vencida"""
    asunto = "Tu membresía ha vencido"
    
    cuerpo = f"""
    <html>
        <body>
            <h2>Hola {nombre},</h2>
            <p>Tu membresía venció el {fecha_vencimiento}.</p>
            <p>Para seguir disfrutando de nuestros servicios, renueva tu membresía.</p>
            <p>¡Te esperamos!</p>
        </body>
    </html>
    """
    
    return enviar_email(destinatario, asunto, cuerpo, html=True)