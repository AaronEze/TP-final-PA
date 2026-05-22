"""
Módulo: models/busqueda.py
Clase Búsqueda - Representa una vacante de empleo
"""

from datetime import datetime
from enum import Enum


class EstadoBusqueda(Enum):
    """Estados posibles de una búsqueda."""
    ABIERTA = "abierta"
    CERRADA = "cerrada"
    EN_REVISION = "en_revision"


class Busqueda:
    """
    Clase Búsqueda que representa una vacante de empleo.
    
    Attributes:
        _id (int): Identificador único
        _titulo_puesto (str): Título del puesto
        _descripcion (str): Descripción de la vacante
        _salario_min (float): Salario mínimo ofrecido
        _salario_max (float): Salario máximo ofrecido
        _skills_requeridos (list[str]): Habilidades requeridas
        _experiencia_minima (int): Años de experiencia mínima
        _estado (EstadoBusqueda): Estado actual de la búsqueda
        _fecha_creacion (datetime): Fecha de creación
        _fecha_cierre (datetime): Fecha de cierre (si aplica)
    """
    
    _contador_ids = 0
    
    def __init__(self, titulo_puesto: str, descripcion: str, 
                 salario_min: float, salario_max: float,
                 skills_requeridos: list, experiencia_minima: int):
        """
        Constructor de Búsqueda.
        
        Args:
            titulo_puesto (str): Título del puesto
            descripcion (str): Descripción de la vacante
            salario_min (float): Salario mínimo
            salario_max (float): Salario máximo
            skills_requeridos (list[str]): Skills requeridos
            experiencia_minima (int): Años mínimos de experiencia
        """
        self._id = self._generar_id()
        self._titulo_puesto = titulo_puesto
        self._descripcion = descripcion
        self._salario_min = salario_min
        self._salario_max = salario_max
        self._skills_requeridos = skills_requeridos.copy()
        self._experiencia_minima = experiencia_minima
        self._estado = EstadoBusqueda.ABIERTA
        self._fecha_creacion = datetime.now()
        self._fecha_cierre = None
    
    @staticmethod
    def _generar_id() -> int:
        """Genera un ID único."""
        Busqueda._contador_ids += 1
        return Busqueda._contador_ids
    
    # ============ GETTERS ============
    
    @property
    def id(self) -> int:
        """Retorna el ID de la búsqueda."""
        return self._id
    
    @property
    def titulo_puesto(self) -> str:
        """Retorna el título del puesto."""
        return self._titulo_puesto
    
    @property
    def descripcion(self) -> str:
        """Retorna la descripción."""
        return self._descripcion
    
    @property
    def salario_min(self) -> float:
        """Retorna el salario mínimo."""
        return self._salario_min
    
    @property
    def salario_max(self) -> float:
        """Retorna el salario máximo."""
        return self._salario_max
    
    @property
    def skills_requeridos(self) -> list:
        """Retorna la lista de skills requeridos."""
        return self._skills_requeridos.copy()
    
    @property
    def experiencia_minima(self) -> int:
        """Retorna la experiencia mínima requerida."""
        return self._experiencia_minima
    
    @property
    def estado(self) -> EstadoBusqueda:
        """Retorna el estado de la búsqueda."""
        return self._estado
    
    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha de creación."""
        return self._fecha_creacion
    
    @property
    def fecha_cierre(self):
        """Retorna la fecha de cierre."""
        return self._fecha_cierre
    
    # ============ SETTERS ============
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoBusqueda):
        """Actualiza el estado de la búsqueda."""
        self._estado = nuevo_estado
        if nuevo_estado == EstadoBusqueda.CERRADA:
            self._fecha_cierre = datetime.now()
    
    # ============ MÉTODOS ============
    
    def obtener_requisitos(self) -> dict:
        """
        Retorna los requisitos de la búsqueda en formato diccionario.
        
        Returns:
            dict: Diccionario con requisitos
        """
        return {
            'titulo': self._titulo_puesto,
            'experiencia_minima': self._experiencia_minima,
            'skills': self._skills_requeridos.copy(),
            'salario_rango': f"${self._salario_min} - ${self._salario_max}"
        }
    
    def candidato_cumple_requisitos(self, candidato) -> dict:
        """
        Verifica si un candidato cumple con los requisitos de la búsqueda.
        
        Args:
            candidato (Candidato): Candidato a evaluar
            
        Returns:
            dict: Diccionario con análisis detallado
        """
        cumple_experiencia = candidato.tiene_experiencia_minima(self._experiencia_minima)
        tiene_skills = candidato.tiene_todas_habilidades(self._skills_requeridos)
        
        skills_faltantes = [s for s in self._skills_requeridos 
                           if not candidato.tiene_habilidad(s)]
        
        resultado = {
            'cumple_experiencia': cumple_experiencia,
            'cumple_skills': tiene_skills,
            'cumple_todos': cumple_experiencia and tiene_skills,
            'skills_faltantes': skills_faltantes,
            'experiencia_candidato': candidato.anos_experiencia,
            'experiencia_requerida': self._experiencia_minima
        }
        
        return resultado
    
    def cerrar_busqueda(self) -> None:
        """Cierra la búsqueda."""
        self.estado = EstadoBusqueda.CERRADA
    
    def reabrirt_busqueda(self) -> None:
        """Reabre la búsqueda."""
        self.estado = EstadoBusqueda.ABIERTA
        self._fecha_cierre = None
    
    def obtener_rango_salario(self) -> str:
        """Retorna el rango de salario formateado."""
        return f"${self._salario_min:,.2f} - ${self._salario_max:,.2f}"
    
    def obtener_info(self) -> str:
        """
        Retorna información detallada de la búsqueda.
        
        Returns:
            str: Información formateada
        """
        info = f"""
        ═══════════════════════════════════════════
        BÚSQUEDA DE EMPLEO
        ═══════════════════════════════════════════
        ID: {self._id}
        Puesto: {self._titulo_puesto}
        Estado: {self._estado.value}
        Descripción: {self._descripcion}
        Experiencia mínima: {self._experiencia_minima} años
        Rango salarial: {self.obtener_rango_salario()}
        Skills requeridos: {', '.join(self._skills_requeridos)}
        Fecha creación: {self._fecha_creacion.strftime('%d/%m/%Y %H:%M')}
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
        """Representación en string."""
        return f"{self._titulo_puesto} (ID: {self._id}, Estado: {self._estado.value})"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"Busqueda(id={self._id}, titulo='{self._titulo_puesto}')"
