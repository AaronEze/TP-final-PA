"""Clase Evaluación - Evaluación de candidatos simplificada"""
from datetime import datetime
from enum import Enum


class ResultadoEvaluacion(Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class Evaluacion:
    """Evaluación de un candidato para una búsqueda"""
    
    _contador_ids = 0
    
    def __init__(self, candidato, busqueda, evaluador: str):
        self._id = self._generar_id()
        self._candidato = candidato
        self._busqueda = busqueda
        self._evaluador = evaluador
        self._resultado = ResultadoEvaluacion.PENDIENTE
        self._puntuacion = 0.0
        self._comentarios = ""
        self._fecha_evaluacion = None
    
    @staticmethod
    def _generar_id() -> int:
        Evaluacion._contador_ids += 1
        return Evaluacion._contador_ids
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def candidato(self):
        return self._candidato
    
    @property
    def busqueda(self):
        return self._busqueda
    
    @property
    def evaluador(self) -> str:
        return self._evaluador
    
    @property
    def resultado(self) -> ResultadoEvaluacion:
        return self._resultado
    
    @property
    def puntuacion(self) -> float:
        return self._puntuacion
    
    @property
    def comentarios(self) -> str:
        return self._comentarios
    
    @property
    def fecha_evaluacion(self) -> datetime:
        return self._fecha_evaluacion # type: ignore
    
    # Métodos
    def evaluar(self, resultado: str, puntuacion: float, comentarios: str = "") -> bool:
        if not (0 <= puntuacion <= 100):
            raise ValueError("Puntuación debe estar entre 0 y 100")
        
        resultado_lower = resultado.lower()
        if resultado_lower == "aprobado":
            self._resultado = ResultadoEvaluacion.APROBADO
        elif resultado_lower == "rechazado":
            self._resultado = ResultadoEvaluacion.RECHAZADO
        else:
            raise ValueError("Resultado debe ser 'aprobado' o 'rechazado'")
        
        self._puntuacion = puntuacion
        self._comentarios = comentarios
        self._fecha_evaluacion = datetime.now()
        return True
    
    def es_aprobado(self) -> bool:
        return self._resultado == ResultadoEvaluacion.APROBADO
    
    def es_rechazado(self) -> bool:
        return self._resultado == ResultadoEvaluacion.RECHAZADO
    
    def esta_pendiente(self) -> bool:
        return self._resultado == ResultadoEvaluacion.PENDIENTE
    
    def obtener_analisis(self) -> dict:
        analisis = self._busqueda.candidato_cumple_requisitos(self._candidato)
        return {
            'candidato_nombre': self._candidato.nombre,
            'puesto': self._busqueda.titulo_puesto,
            'resultado': self._resultado.value,
            'puntuacion': self._puntuacion,
            'cumple_requisitos': analisis['cumple_todos'],
            'cumple_experiencia': analisis['cumple_experiencia'],
            'cumple_skills': analisis['cumple_skills'],
            'skills_faltantes': analisis['skills_faltantes'],
            'comentarios': self._comentarios,
            'evaluador': self._evaluador,
            'fecha': self._fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self._fecha_evaluacion else "Pendiente"
        }
    
    def to_dict(self) -> dict:
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
        return f"Evaluación {self._id}: {self._candidato.nombre} - {self._resultado.value}"
