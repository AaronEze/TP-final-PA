"""
Módulo: models/candidato.py
Clase Candidato - Herencia de Persona
"""

from models.persona import Persona
from datetime import datetime
from enum import Enum


class EstadoCandidato(Enum):
    """Estados posibles de un candidato."""
    REGISTRADO = "registrado"
    EVALUADO = "evaluado"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class Candidato(Persona):
    """
    Clase Candidato que hereda de Persona.
    Representa a un candidato que se postula a búsquedas de empleo.
    
    Attributes:
        _anos_experiencia (int): Años de experiencia laboral
        _habilidades (list[str]): Lista de habilidades técnicas
        _cv (str): Texto del CV o perfil profesional
        _estado (EstadoCandidato): Estado actual del candidato
        _fecha_registro (datetime): Fecha de registro como candidato
    """
    
    def __init__(self, nombre: str, email: str, telefono: str, 
                 anos_experiencia: int, cv: str):
        """
        Constructor de Candidato.
        
        Args:
            nombre (str): Nombre completo del candidato
            email (str): Correo electrónico
            telefono (str): Número de teléfono
            anos_experiencia (int): Años de experiencia laboral
            cv (str): Texto del CV o descripción profesional
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Llamar al constructor de la clase padre (Persona)
        super().__init__(nombre, email, telefono)
        
        # Atributos específicos de Candidato (Encapsulamiento)
        self._anos_experiencia = anos_experiencia
        self._habilidades = []  # Lista vacía inicialmente
        self._cv = cv
        self._estado = EstadoCandidato.REGISTRADO
        self._fecha_postulacion = datetime.now()
    
    # ============ GETTERS ============
    
    @property
    def anos_experiencia(self) -> int:
        """Retorna los años de experiencia."""
        return self._anos_experiencia
    
    @property
    def habilidades(self) -> list:
        """Retorna la lista de habilidades."""
        return self._habilidades.copy()  # Devolver copia para encapsulamiento
    
    @property
    def cv(self) -> str:
        """Retorna el CV del candidato."""
        return self._cv
    
    @property
    def estado(self) -> EstadoCandidato:
        """Retorna el estado del candidato."""
        return self._estado
    
    @property
    def fecha_postulacion(self) -> datetime:
        """Retorna la fecha de postulación."""
        return self._fecha_postulacion
    
    # ============ SETTERS ============
    
    @anos_experiencia.setter
    def anos_experiencia(self, anos: int):
        """
        Actualiza los años de experiencia.
        
        Args:
            anos (int): Nuevos años de experiencia
            
        Raises:
            ValueError: Si años es negativo
        """
        if anos < 0:
            raise ValueError("Los años de experiencia no pueden ser negativos")
        self._anos_experiencia = anos
    
    @cv.setter
    def cv(self, nuevo_cv: str):
        """Actualiza el CV del candidato."""
        self._cv = nuevo_cv
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoCandidato):
        """Actualiza el estado del candidato."""
        self._estado = nuevo_estado
    
    # ============ MÉTODOS PRINCIPALES ============
    
    def agregar_habilidad(self, habilidad: str) -> None:
        """
        Agrega una habilidad a la lista de habilidades del candidato.
        
        Args:
            habilidad (str): Nombre de la habilidad a agregar
        """
        if habilidad and habilidad not in self._habilidades:
            self._habilidades.append(habilidad)
    
    def agregar_multiples_habilidades(self, habilidades: list) -> None:
        """
        Agrega múltiples habilidades de una vez.
        
        Args:
            habilidades (list[str]): Lista de habilidades a agregar
        """
        for habilidad in habilidades:
            self.agregar_habilidad(habilidad)
    
    def eliminar_habilidad(self, habilidad: str) -> bool:
        """
        Elimina una habilidad de la lista.
        
        Args:
            habilidad (str): Habilidad a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if habilidad in self._habilidades:
            self._habilidades.remove(habilidad)
            return True
        return False
    
    def tiene_experiencia_minima(self, anos_minimos: int) -> bool:
        """
        Verifica si el candidato cumple con la experiencia mínima requerida.
        
        Args:
            anos_minimos (int): Años mínimos requeridos
            
        Returns:
            bool: True si cumple, False en caso contrario
        """
        return self._anos_experiencia >= anos_minimos
    
    def tiene_habilidad(self, habilidad: str) -> bool:
        """
        Verifica si el candidato tiene una habilidad específica.
        
        Args:
            habilidad (str): Habilidad a buscar
            
        Returns:
            bool: True si la tiene, False en caso contrario
        """
        return habilidad.lower() in [h.lower() for h in self._habilidades]
    
    def tiene_todas_habilidades(self, habilidades_requeridas: list) -> bool:
        """
        Verifica si el candidato tiene TODAS las habilidades requeridas.
        
        Args:
            habilidades_requeridas (list[str]): Lista de habilidades a verificar
            
        Returns:
            bool: True si tiene todas, False en caso contrario
        """
        for habilidad in habilidades_requeridas:
            if not self.tiene_habilidad(habilidad):
                return False
        return True
    
    # ============ POLIMORFISMO - Override de métodos abstractos ============
    
    def obtener_info(self) -> str:
        """
        Sobrescribe el método abstracto de Persona.
        Retorna información detallada del candidato.
        
        Returns:
            str: Información formateada del candidato
        """
        info = f"""
        ═══════════════════════════════════════════
        DATOS DEL CANDIDATO
        ═══════════════════════════════════════════
        ID: {self._id}
        Nombre: {self._nombre}
        Email: {self._email}
        Teléfono: {self._telefono}
        Experiencia: {self._anos_experiencia} años
        Estado: {self._estado.value}
        Habilidades: {', '.join(self._habilidades) if self._habilidades else 'Sin habilidades registradas'}
        Fecha de postulación: {self._fecha_postulacion.strftime('%d/%m/%Y %H:%M')}
        ═══════════════════════════════════════════
        """
        return info
    
    def validar(self) -> bool:
        """
        Sobrescribe el método abstracto de Persona.
        Valida que los datos del candidato sean correctos.
        
        Returns:
            bool: True si todos los datos son válidos, False en caso contrario
        """
        validaciones = {
            'nombre_valido': len(self._nombre.strip()) > 0,
            'email_valido': self._email is not None,
            'telefono_valido': len(self._telefono.strip()) > 0,
            'experiencia_valida': self._anos_experiencia >= 0,
            'cv_valido': len(self._cv.strip()) > 0
        }
        
        # Retorna True solo si TODAS las validaciones son correctas
        return all(validaciones.values())
    
    # ============ MÉTODO PARA REPORTES ============
    
    def obtener_info_compacta(self) -> dict:
        """
        Retorna la información del candidato en formato diccionario.
        Útil para JSON, reportes, etc.
        
        Returns:
            dict: Diccionario con datos del candidato
        """
        return {
            'id': self._id,
            'nombre': self._nombre,
            'email': self._email,
            'telefono': self._telefono,
            'anos_experiencia': self._anos_experiencia,
            'habilidades': self._habilidades.copy(),
            'estado': self._estado.value,
            'fecha_postulacion': self._fecha_postulacion.isoformat()
        }
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"{self._nombre} ({self._anos_experiencia} años exp, {self._estado.value})"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"Candidato(id={self._id}, nombre='{self._nombre}', exp={self._anos_experiencia})"
