"""Service de Progreso (extensión de progreso_fisico_service)"""
from typing import List, Dict, Any
from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.progreso_fisico import ProgresoFisicoRepository
from app.repositories.usuario import UsuarioRepository
from app.models.progreso_fisico import ProgresoFisico


class ProgresoService:
    """Servicio extendido para análisis de progreso físico"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProgresoFisicoRepository(db)
        self.usuario_repo = UsuarioRepository(db)
    
    # ========================================
    # ANÁLISIS DE PROGRESO
    # ========================================
    
    def calcular_progreso(
        self,
        usuario_id: int,
        dias: int = 30
    ) -> Dict[str, Any]:
        """
        Calcula el progreso de un usuario en los últimos N días.
        
        Args:
            usuario_id: ID del usuario
            dias: Número de días a analizar
            
        Returns:
            Diccionario con análisis de progreso
        """
        # Obtener registros del período
        fecha_inicio = date.today() - timedelta(days=dias)
        registros = self.repo.get_by_rango_fechas(usuario_id, fecha_inicio, date.today())
        
        if len(registros) < 2:
            return {
                "mensaje": "Se necesitan al menos 2 registros para calcular progreso",
                "registros_encontrados": len(registros)
            }
        
        # Ordenar por fecha
        registros.sort(key=lambda x: x.fecha_registro)
        
        primer_registro = registros[0]
        ultimo_registro = registros[-1]
        
        return {
            "periodo_dias": dias,
            "total_registros": len(registros),
            "primer_registro": primer_registro.fecha_registro,
            "ultimo_registro": ultimo_registro.fecha_registro,
            "cambios": self._calcular_cambios(primer_registro, ultimo_registro),
            "promedios": self._calcular_promedios(registros),
            "tendencias": self._calcular_tendencias(registros)
        }
    
    def _calcular_cambios(
        self,
        registro_inicial: ProgresoFisico,
        registro_final: ProgresoFisico
    ) -> Dict[str, Any]:
        """Calcula cambios entre dos registros"""
        cambios = {}
        
        # Peso
        if registro_inicial.peso and registro_final.peso:
            cambios["peso"] = {
                "inicial": float(registro_inicial.peso),
                "final": float(registro_final.peso),
                "cambio": float(registro_final.peso - registro_inicial.peso),
                "porcentaje": round(((registro_final.peso - registro_inicial.peso) / registro_inicial.peso) * 100, 2)
            }
        
        # Porcentaje de grasa
        if registro_inicial.porcentaje_grasa and registro_final.porcentaje_grasa:
            cambios["porcentaje_grasa"] = {
                "inicial": float(registro_inicial.porcentaje_grasa),
                "final": float(registro_final.porcentaje_grasa),
                "cambio": float(registro_final.porcentaje_grasa - registro_inicial.porcentaje_grasa)
            }
        
        # Masa muscular
        if registro_inicial.masa_muscular and registro_final.masa_muscular:
            cambios["masa_muscular"] = {
                "inicial": float(registro_inicial.masa_muscular),
                "final": float(registro_final.masa_muscular),
                "cambio": float(registro_final.masa_muscular - registro_inicial.masa_muscular),
                "porcentaje": round(((registro_final.masa_muscular - registro_inicial.masa_muscular) / registro_inicial.masa_muscular) * 100, 2)
            }
        
        # IMC
        if registro_inicial.imc and registro_final.imc:
            cambios["imc"] = {
                "inicial": float(registro_inicial.imc),
                "final": float(registro_final.imc),
                "cambio": float(registro_final.imc - registro_inicial.imc)
            }
        
        # Circunferencias
        medidas = ["circunferencia_pecho", "circunferencia_cintura", "circunferencia_cadera", 
                   "circunferencia_brazo", "circunferencia_pierna"]
        
        for medida in medidas:
            inicial = getattr(registro_inicial, medida)
            final = getattr(registro_final, medida)
            
            if inicial and final:
                cambios[medida] = {
                    "inicial": float(inicial),
                    "final": float(final),
                    "cambio": float(final - inicial)
                }
        
        return cambios
    
    def _calcular_promedios(self, registros: List[ProgresoFisico]) -> Dict[str, float]:
        """Calcula promedios de las mediciones"""
        promedios = {}
        campos = ["peso", "porcentaje_grasa", "masa_muscular", "imc"]
        
        for campo in campos:
            valores = [float(getattr(r, campo)) for r in registros if getattr(r, campo)]
            if valores:
                promedios[f"{campo}_promedio"] = round(sum(valores) / len(valores), 2)
        
        return promedios
    
    def _calcular_tendencias(self, registros: List[ProgresoFisico]) -> Dict[str, str]:
        """Determina tendencias (subiendo, bajando, estable)"""
        if len(registros) < 3:
            return {}
        
        tendencias = {}
        campos = ["peso", "porcentaje_grasa", "masa_muscular"]
        
        for campo in campos:
            valores = [float(getattr(r, campo)) for r in registros if getattr(r, campo)]
            
            if len(valores) >= 3:
                # Comparar primeros vs últimos valores
                primer_tercio = sum(valores[:len(valores)//3]) / (len(valores)//3)
                ultimo_tercio = sum(valores[-len(valores)//3:]) / (len(valores)//3)
                
                diferencia = ultimo_tercio - primer_tercio
                
                if abs(diferencia) < 0.5:  # Umbral de estabilidad
                    tendencias[campo] = "estable"
                elif diferencia > 0:
                    tendencias[campo] = "aumentando"
                else:
                    tendencias[campo] = "disminuyendo"
        
        return tendencias
    
    # ========================================
    # COMPARACIONES
    # ========================================
    
    def comparar_registros(
        self,
        usuario_id: int,
        registro1_id: int,
        registro2_id: int
    ) -> Dict[str, Any]:
        """
        Compara dos registros específicos.
        
        Args:
            usuario_id: ID del usuario
            registro1_id: ID del primer registro
            registro2_id: ID del segundo registro
            
        Returns:
            Diccionario con comparación
        """
        registro1 = self.repo.get_by_id(registro1_id)
        registro2 = self.repo.get_by_id(registro2_id)
        
        # Validar que pertenezcan al usuario
        if not registro1 or registro1.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Primer registro no encontrado"
            )
        
        if not registro2 or registro2.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Segundo registro no encontrado"
            )
        
        # Ordenar por fecha
        if registro1.fecha_registro > registro2.fecha_registro:
            registro1, registro2 = registro2, registro1
        
        return {
            "registro_inicial": {
                "id": registro1.id,
                "fecha": registro1.fecha_registro
            },
            "registro_final": {
                "id": registro2.id,
                "fecha": registro2.fecha_registro
            },
            "dias_diferencia": (registro2.fecha_registro - registro1.fecha_registro).days,
            "cambios": self._calcular_cambios(registro1, registro2)
        }
    
    # ========================================
    # OBJETIVOS Y METAS
    # ========================================
    
    def calcular_objetivos(
        self,
        usuario_id: int,
        peso_objetivo: float = None,
        grasa_objetivo: float = None,
        musculo_objetivo: float = None
    ) -> Dict[str, Any]:
        """
        Calcula qué tan cerca está el usuario de sus objetivos.
        
        Args:
            usuario_id: ID del usuario
            peso_objetivo: Peso objetivo en kg
            grasa_objetivo: Porcentaje de grasa objetivo
            musculo_objetivo: Masa muscular objetivo en kg
            
        Returns:
            Diccionario con progreso hacia objetivos
        """
        ultimo = self.repo.get_ultimo_registro(usuario_id)
        
        if not ultimo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay registros de progreso"
            )
        
        objetivos = {}
        
        if peso_objetivo and ultimo.peso:
            diferencia = float(ultimo.peso) - peso_objetivo
            objetivos["peso"] = {
                "actual": float(ultimo.peso),
                "objetivo": peso_objetivo,
                "diferencia": round(diferencia, 2),
                "porcentaje_completado": round((1 - abs(diferencia) / peso_objetivo) * 100, 2) if peso_objetivo > 0 else 0,
                "alcanzado": abs(diferencia) <= 1.0  # Tolerancia de 1 kg
            }
        
        if grasa_objetivo and ultimo.porcentaje_grasa:
            diferencia = float(ultimo.porcentaje_grasa) - grasa_objetivo
            objetivos["grasa"] = {
                "actual": float(ultimo.porcentaje_grasa),
                "objetivo": grasa_objetivo,
                "diferencia": round(diferencia, 2),
                "alcanzado": abs(diferencia) <= 2.0  # Tolerancia de 2%
            }
        
        if musculo_objetivo and ultimo.masa_muscular:
            diferencia = musculo_objetivo - float(ultimo.masa_muscular)
            objetivos["musculo"] = {
                "actual": float(ultimo.masa_muscular),
                "objetivo": musculo_objetivo,
                "diferencia": round(diferencia, 2),
                "porcentaje_completado": round((float(ultimo.masa_muscular) / musculo_objetivo) * 100, 2) if musculo_objetivo > 0 else 0,
                "alcanzado": diferencia <= 1.0  # Tolerancia de 1 kg
            }
        
        return {
            "fecha_ultimo_registro": ultimo.fecha_registro,
            "objetivos": objetivos
        }
    
    # ========================================
    # REPORTES
    # ========================================
    
    def generar_reporte_mensual(self, usuario_id: int, mes: int, anio: int) -> Dict[str, Any]:
        """
        Genera un reporte mensual de progreso.
        
        Args:
            usuario_id: ID del usuario
            mes: Mes (1-12)
            anio: Año
            
        Returns:
            Diccionario con reporte mensual
        """
        from calendar import monthrange
        
        # Calcular fechas del mes
        dias_mes = monthrange(anio, mes)[1]
        fecha_inicio = date(anio, mes, 1)
        fecha_fin = date(anio, mes, dias_mes)
        
        registros = self.repo.get_by_rango_fechas(usuario_id, fecha_inicio, fecha_fin)
        
        if not registros:
            return {
                "mes": mes,
                "anio": anio,
                "registros": 0,
                "mensaje": "No hay registros en este mes"
            }
        
        registros.sort(key=lambda x: x.fecha_registro)
        
        return {
            "mes": mes,
            "anio": anio,
            "total_registros": len(registros),
            "primer_registro": registros[0].fecha_registro,
            "ultimo_registro": registros[-1].fecha_registro,
            "cambios_mes": self._calcular_cambios(registros[0], registros[-1]) if len(registros) >= 2 else {},
            "promedios": self._calcular_promedios(registros)
        }