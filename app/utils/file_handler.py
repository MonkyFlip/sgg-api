"""Manejador de archivos - Carga, validación y almacenamiento"""
import os
import uuid
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from fastapi import UploadFile

# Configuración
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
    'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx'],
    'all': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.pdf', '.doc', '.docx', '.xls', '.xlsx']
}

class FileHandler:
    """Clase para manejar operaciones con archivos"""
    
    def __init__(self, upload_dir: str = UPLOAD_DIR):
        self.upload_dir = upload_dir
        self._ensure_upload_dir()
    
    def _ensure_upload_dir(self):
        """Crea el directorio de uploads si no existe"""
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def generar_nombre_unico(self, filename: str, prefijo: str = "") -> str:
        """Genera un nombre único para el archivo"""
        extension = Path(filename).suffix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        uuid_corto = str(uuid.uuid4())[:8]
        
        if prefijo:
            return f"{prefijo}_{timestamp}_{uuid_corto}{extension}"
        return f"{timestamp}_{uuid_corto}{extension}"
    
    def validar_extension(self, filename: str, tipo: str = 'all') -> bool:
        """Valida la extensión del archivo"""
        extension = Path(filename).suffix.lower()
        extensiones_permitidas = ALLOWED_EXTENSIONS.get(tipo, ALLOWED_EXTENSIONS['all'])
        return extension in extensiones_permitidas
    
    def validar_tamano(self, file_size: int, max_size: int = MAX_FILE_SIZE) -> bool:
        """Valida el tamaño del archivo"""
        return file_size <= max_size
    
    async def guardar_archivo(
        self,
        file: UploadFile,
        subdirectorio: str = "",
        prefijo: str = ""
    ) -> dict:
        """
        Guarda un archivo subido.
        
        Args:
            file: Archivo subido
            subdirectorio: Subdirectorio dentro de uploads
            prefijo: Prefijo para el nombre del archivo
            
        Returns:
            Dict con información del archivo guardado
        """
        # Validar extensión
        if not self.validar_extension(file.filename):
            raise ValueError(f"Extensión de archivo no permitida: {file.filename}")
        
        # Leer contenido
        contenido = await file.read()
        
        # Validar tamaño
        if not self.validar_tamano(len(contenido)):
            raise ValueError(f"Archivo muy grande. Máximo: {MAX_FILE_SIZE / 1024 / 1024} MB")
        
        # Generar nombre único
        nombre_unico = self.generar_nombre_unico(file.filename, prefijo)
        
        # Crear ruta completa
        if subdirectorio:
            directorio_completo = os.path.join(self.upload_dir, subdirectorio)
            os.makedirs(directorio_completo, exist_ok=True)
            ruta_completa = os.path.join(directorio_completo, nombre_unico)
            ruta_relativa = os.path.join(subdirectorio, nombre_unico)
        else:
            ruta_completa = os.path.join(self.upload_dir, nombre_unico)
            ruta_relativa = nombre_unico
        
        # Guardar archivo
        with open(ruta_completa, 'wb') as f:
            f.write(contenido)
        
        return {
            "filename": nombre_unico,
            "original_filename": file.filename,
            "path": ruta_relativa,
            "full_path": ruta_completa,
            "size": len(contenido),
            "content_type": file.content_type
        }
    
    def eliminar_archivo(self, ruta: str) -> bool:
        """Elimina un archivo"""
        try:
            ruta_completa = os.path.join(self.upload_dir, ruta)
            if os.path.exists(ruta_completa):
                os.remove(ruta_completa)
                return True
            return False
        except Exception:
            return False
    
    def obtener_url(self, ruta: str, base_url: str = "/uploads") -> str:
        """Genera URL pública del archivo"""
        return f"{base_url}/{ruta}"

# Funciones helper para usar sin instanciar la clase
_handler = FileHandler()

async def guardar_archivo(file: UploadFile, subdirectorio: str = "", prefijo: str = "") -> dict:
    """Guarda un archivo (función helper)"""
    return await _handler.guardar_archivo(file, subdirectorio, prefijo)

def eliminar_archivo(ruta: str) -> bool:
    """Elimina un archivo (función helper)"""
    return _handler.eliminar_archivo(ruta)

def validar_archivo(filename: str, tipo: str = 'all') -> bool:
    """Valida un archivo (función helper)"""
    return _handler.validar_extension(filename, tipo)

def obtener_url_archivo(ruta: str, base_url: str = "/uploads") -> str:
    """Obtiene URL de un archivo (función helper)"""
    return _handler.obtener_url(ruta, base_url)