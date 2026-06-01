"""Clase Búsqueda - Vacante de empleo simplificada"""
from datetime import datetime
from enum import Enum


class EstadoBusqueda(Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"
    EN_REVISION = "en_revision"


class Busqueda:
    """Representa una vacante de empleo"""
    
    _contador_ids = 0
    
    def __init__(self, titulo_puesto: str, descripcion: str, 
                 salario_min: float, salario_max: float,
                 skills_requeridos: list, experiencia_minima: int):
        self._id = self._generar_id()
        self._titulo_puesto = titulo_puesto
        self._descripcion = descripcion
        self._salario_min = salario_min
        self._salario_max = salario_max
        self._skills_requeridos = skills_requeridos.copy()
        self._experiencia_minima = experiencia_minima
        self._estado = EstadoBusqueda.ABIERTA
        self._fecha_creacion = datetime.now()
    
    @staticmethod
    def _generar_id() -> int:
        Busqueda._contador_ids += 1
        return Busqueda._contador_ids
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def titulo_puesto(self) -> str:
        return self._titulo_puesto
    
    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @property
    def salario_min(self) -> float:
        return self._salario_min
    
    @property
    def salario_max(self) -> float:
        return self._salario_max
    
    @property
    def skills_requeridos(self) -> list:
        return self._skills_requeridos.copy()
    
    @property
    def experiencia_minima(self) -> int:
        return self._experiencia_minima
    
    @property
    def estado(self) -> EstadoBusqueda:
        return self._estado
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoBusqueda):
        self._estado = nuevo_estado
    
    # Métodos
    def candidato_cumple_requisitos(self, candidato) -> dict:
        cumple_exp = candidato.tiene_experiencia_minima(self._experiencia_minima)
        cumple_skills = candidato.tiene_todas_habilidades(self._skills_requeridos)
        skills_faltantes = [s for s in self._skills_requeridos 
                           if not candidato.tiene_habilidad(s)]
        
        return {
            'cumple_experiencia': cumple_exp,
            'cumple_skills': cumple_skills,
            'cumple_todos': cumple_exp and cumple_skills,
            'skills_faltantes': skills_faltantes,
            'experiencia_candidato': candidato.anos_experiencia,
            'experiencia_requerida': self._experiencia_minima
        }
    
    def cerrar(self) -> None:
        self.estado = EstadoBusqueda.CERRADA
    
    def obtener_rango_salario(self) -> str:
        return f"${self._salario_min:,.2f} - ${self._salario_max:,.2f}"
    
    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'titulo_puesto': self._titulo_puesto,
            'descripcion': self._descripcion,
            'salario_min': self._salario_min,
            'salario_max': self._salario_max,
            'skills_requeridos': self._skills_requeridos.copy(),
            'experiencia_minima': self._experiencia_minima,
            'estado': self._estado.value,
            'fecha_creacion': self._fecha_creacion.isoformat()
        }
    
    def __str__(self) -> str:
        return f"{self._titulo_puesto} (ID: {self._id}, {self._estado.value})"
