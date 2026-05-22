"""
Módulo: models/evaluacion.py
Clase Evaluación - Composición de Candidato + Búsqueda
"""

from datetime import datetime
from enum import Enum


class ResultadoEvaluacion(Enum):
    """Resultados posibles de una evaluación."""
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class Evaluacion:
    """
    Clase Evaluación que representa la evaluación de un candidato para una búsqueda.
    Ejemplo de COMPOSICIÓN: contiene referencias a Candidato y Búsqueda.
    
    Attributes:
        _id (int): Identificador único
        _candidato (Candidato): Referencia al candidato [COMPOSICIÓN]
        _busqueda (Búsqueda): Referencia a la búsqueda [COMPOSICIÓN]
        _evaluador (str): Nombre del evaluador
        _resultado (ResultadoEvaluacion): Resultado de la evaluación
        _puntuacion (float): Puntuación de 0 a 100
        _comentarios (str): Comentarios de la evaluación
        _fecha_evaluacion (datetime): Fecha de evaluación
    """
    
    _contador_ids = 0
    
    def __init__(self, candidato, busqueda, evaluador: str):
        """
        Constructor de Evaluación.
        
        Args:
            candidato (Candidato): Candidato a evaluar [COMPOSICIÓN]
            busqueda (Búsqueda): Búsqueda a la que se postula [COMPOSICIÓN]
            evaluador (str): Nombre del evaluador
        """
        self._id = self._generar_id()
        self._candidato = candidato  # COMPOSICIÓN
        self._busqueda = busqueda    # COMPOSICIÓN
        self._evaluador = evaluador
        self._resultado = ResultadoEvaluacion.PENDIENTE
        self._puntuacion = 0.0
        self._comentarios = ""
        self._fecha_evaluacion = None
    
    @staticmethod
    def _generar_id() -> int:
        """Genera un ID único."""
        Evaluacion._contador_ids += 1
        return Evaluacion._contador_ids
    
    # ============ GETTERS ============
    
    @property
    def id(self) -> int:
        """Retorna el ID de la evaluación."""
        return self._id
    
    @property
    def candidato(self):
        """Retorna la referencia al candidato."""
        return self._candidato
    
    @property
    def busqueda(self):
        """Retorna la referencia a la búsqueda."""
        return self._busqueda
    
    @property
    def evaluador(self) -> str:
        """Retorna el nombre del evaluador."""
        return self._evaluador
    
    @property
    def resultado(self) -> ResultadoEvaluacion:
        """Retorna el resultado de la evaluación."""
        return self._resultado
    
    @property
    def puntuacion(self) -> float:
        """Retorna la puntuación."""
        return self._puntuacion
    
    @property
    def comentarios(self) -> str:
        """Retorna los comentarios."""
        return self._comentarios
    
    @property
    def fecha_evaluacion(self) -> datetime:
        """Retorna la fecha de evaluación."""
        return self._fecha_evaluacion
    
    # ============ SETTERS ============
    
    @evaluador.setter
    def evaluador(self, nuevo_evaluador: str):
        """Actualiza el evaluador."""
        self._evaluador = nuevo_evaluador
    
    # ============ MÉTODOS ============
    
    def evaluar(self, resultado: str, puntuacion: float, comentarios: str = "") -> bool:
        """
        Realiza la evaluación del candidato.
        
        Args:
            resultado (str): "aprobado" o "rechazado"
            puntuacion (float): Puntuación de 0 a 100
            comentarios (str): Comentarios adicionales
            
        Returns:
            bool: True si la evaluación se guardó correctamente
        """
        if puntuacion < 0 or puntuacion > 100:
            raise ValueError("La puntuación debe estar entre 0 y 100")
        
        if resultado.lower() == "aprobado":
            self._resultado = ResultadoEvaluacion.APROBADO
        elif resultado.lower() == "rechazado":
            self._resultado = ResultadoEvaluacion.RECHAZADO
        else:
            raise ValueError("Resultado debe ser 'aprobado' o 'rechazado'")
        
        self._puntuacion = puntuacion
        self._comentarios = comentarios
        self._fecha_evaluacion = datetime.now()
        
        return True
    
    def es_aprobado(self) -> bool:
        """
        Verifica si la evaluación fue aprobada.
        
        Returns:
            bool: True si fue aprobada
        """
        return self._resultado == ResultadoEvaluacion.APROBADO
    
    def es_rechazado(self) -> bool:
        """
        Verifica si la evaluación fue rechazada.
        
        Returns:
            bool: True si fue rechazada
        """
        return self._resultado == ResultadoEvaluacion.RECHAZADO
    
    def esta_pendiente(self) -> bool:
        """
        Verifica si la evaluación está pendiente.
        
        Returns:
            bool: True si está pendiente
        """
        return self._resultado == ResultadoEvaluacion.PENDIENTE
    
    def obtener_analisis(self) -> dict:
        """
        Retorna un análisis completo de la evaluación.
        
        Returns:
            dict: Análisis detallado
        """
        analisis_requisitos = self._busqueda.candidato_cumple_requisitos(self._candidato)
        
        return {
            'candidato_nombre': self._candidato.nombre,
            'puesto': self._busqueda.titulo_puesto,
            'resultado': self._resultado.value,
            'puntuacion': self._puntuacion,
            'cumple_requisitos': analisis_requisitos['cumple_todos'],
            'cumple_experiencia': analisis_requisitos['cumple_experiencia'],
            'cumple_skills': analisis_requisitos['cumple_skills'],
            'skills_faltantes': analisis_requisitos['skills_faltantes'],
            'comentarios': self._comentarios,
            'evaluador': self._evaluador,
            'fecha': self._fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self._fecha_evaluacion else "Pendiente"
        }
    
    def obtener_info(self) -> str:
        """
        Retorna información formateada de la evaluación.
        
        Returns:
            str: Información completa
        """
        info = f"""
        ═══════════════════════════════════════════
        EVALUACIÓN
        ═══════════════════════════════════════════
        ID: {self._id}
        Candidato: {self._candidato.nombre}
        Puesto: {self._busqueda.titulo_puesto}
        Evaluador: {self._evaluador}
        Resultado: {self._resultado.value}
        Puntuación: {self._puntuacion}/100
        Comentarios: {self._comentarios if self._comentarios else "Sin comentarios"}
        Fecha: {self._fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self._fecha_evaluacion else "Pendiente"}
        ═══════════════════════════════════════════
        """
        return info
    
    def obtener_info_compacta(self) -> dict:
        """
        Retorna la información en formato diccionario.
        
        Returns:
            dict: Información compacta
        """
        return {
            'id': self._id,
            'candidato_id': self._candidato.id,
            'candidato_nombre': self._candidato.nombre,
            'busqueda_id': self._busqueda.id,
            'puesto': self._busqueda.titulo_puesto,
            'evaluador': self._evaluador,
            'resultado': self._resultado.value,
            'puntuacion': self._puntuacion,
            'comentarios': self._comentarios,
            'fecha_evaluacion': self._fecha_evaluacion.isoformat() if self._fecha_evaluacion else None
        }
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"Evaluación {self._id}: {self._candidato.nombre} para {self._busqueda.titulo_puesto} - {self._resultado.value}"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"Evaluacion(id={self._id}, candidato_id={self._candidato.id}, busqueda_id={self._busqueda.id})"
