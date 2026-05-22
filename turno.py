"""
Módulo: models/turno.py
Clase Turno - Entrevista agendada (COMPOSICIÓN con Evaluación)
"""

from datetime import date, datetime, time
from enum import Enum


class EstadoTurno(Enum):
    """Estados posibles de un turno."""
    AGENDADO = "agendado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"
    NO_PRESENTADO = "no_presentado"


class Turno:
    """
    Clase Turno que representa una entrevista agendada.
    Ejemplo de COMPOSICIÓN: contiene una referencia a Evaluación.
    
    Attributes:
        _id (int): Identificador único
        _evaluacion (Evaluacion): Referencia a la evaluación [COMPOSICIÓN]
        _fecha (date): Fecha de la entrevista
        _hora (str): Hora de la entrevista (formato HH:MM)
        _entrevistador (str): Nombre del entrevistador
        _sala (str): Sala donde se realizará la entrevista
        _estado (EstadoTurno): Estado actual del turno
        _observaciones (str): Observaciones adicionales
        _fecha_creacion (datetime): Fecha de creación del turno
        _fecha_cancelacion (datetime): Fecha de cancelación (si aplica)
    """
    
    _contador_ids = 0
    
    def __init__(self, evaluacion, fecha: date, hora: str, 
                 entrevistador: str, sala: str):
        """
        Constructor de Turno.
        
        Args:
            evaluacion (Evaluacion): Evaluación asociada [COMPOSICIÓN]
            fecha (date): Fecha de la entrevista
            hora (str): Hora en formato 'HH:MM'
            entrevistador (str): Nombre del entrevistador
            sala (str): Sala donde se realizará
        """
        self._id = self._generar_id()
        self._evaluacion = evaluacion  # COMPOSICIÓN
        self._fecha = fecha
        self._hora = hora
        self._entrevistador = entrevistador
        self._sala = sala
        self._estado = EstadoTurno.AGENDADO
        self._observaciones = ""
        self._fecha_creacion = datetime.now()
        self._fecha_cancelacion = None
    
    @staticmethod
    def _generar_id() -> int:
        """Genera un ID único."""
        Turno._contador_ids += 1
        return Turno._contador_ids
    
    # ============ GETTERS ============
    
    @property
    def id(self) -> int:
        """Retorna el ID del turno."""
        return self._id
    
    @property
    def evaluacion(self):
        """Retorna la evaluación asociada."""
        return self._evaluacion
    
    @property
    def fecha(self) -> date:
        """Retorna la fecha del turno."""
        return self._fecha
    
    @property
    def hora(self) -> str:
        """Retorna la hora del turno."""
        return self._hora
    
    @property
    def entrevistador(self) -> str:
        """Retorna el nombre del entrevistador."""
        return self._entrevistador
    
    @property
    def sala(self) -> str:
        """Retorna la sala del turno."""
        return self._sala
    
    @property
    def estado(self) -> EstadoTurno:
        """Retorna el estado del turno."""
        return self._estado
    
    @property
    def observaciones(self) -> str:
        """Retorna las observaciones."""
        return self._observaciones
    
    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la fecha de creación."""
        return self._fecha_creacion
    
    @property
    def fecha_cancelacion(self) -> datetime:
        """Retorna la fecha de cancelación."""
        return self._fecha_cancelacion
    
    # ============ SETTERS ============
    
    @entrevistador.setter
    def entrevistador(self, nuevo_entrevistador: str):
        """Actualiza el entrevistador."""
        if self._estado == EstadoTurno.AGENDADO:
            self._entrevistador = nuevo_entrevistador
    
    @sala.setter
    def sala(self, nueva_sala: str):
        """Actualiza la sala."""
        if self._estado == EstadoTurno.AGENDADO:
            self._sala = nueva_sala
    
    # ============ MÉTODOS ============
    
    def agendar(self) -> bool:
        """
        Confirma el agendamiento del turno.
        
        Returns:
            bool: True si se agendó correctamente
        """
        if self._estado == EstadoTurno.AGENDADO:
            return True
        return False
    
    def cancelar(self, motivo: str = "") -> bool:
        """
        Cancela el turno.
        
        Args:
            motivo (str): Motivo de la cancelación
            
        Returns:
            bool: True si se canceló correctamente
        """
        if self._estado in [EstadoTurno.COMPLETADO, EstadoTurno.CANCELADO]:
            return False
        
        self._estado = EstadoTurno.CANCELADO
        self._observaciones = motivo
        self._fecha_cancelacion = datetime.now()
        return True
    
    def completar(self, observaciones: str = "") -> bool:
        """
        Marca el turno como completado.
        
        Args:
            observaciones (str): Observaciones de la entrevista
            
        Returns:
            bool: True si se completó correctamente
        """
        if self._estado != EstadoTurno.AGENDADO:
            return False
        
        self._estado = EstadoTurno.COMPLETADO
        self._observaciones = observaciones
        return True
    
    def marcar_no_presentado(self, observaciones: str = "") -> bool:
        """
        Marca el turno como no presentado.
        
        Args:
            observaciones (str): Observaciones
            
        Returns:
            bool: True si se marcó correctamente
        """
        if self._estado != EstadoTurno.AGENDADO:
            return False
        
        self._estado = EstadoTurno.NO_PRESENTADO
        self._observaciones = observaciones
        return True
    
    def es_disponible(self) -> bool:
        """
        Verifica si el turno aún está disponible (no cancelado ni completado).
        
        Returns:
            bool: True si está disponible
        """
        return self._estado == EstadoTurno.AGENDADO
    
    def es_futuro(self) -> bool:
        """
        Verifica si el turno es futuro.
        
        Returns:
            bool: True si es futuro
        """
        return self._fecha >= date.today()
    
    def obtener_datetime(self) -> datetime:
        """
        Retorna un datetime del turno.
        
        Returns:
            datetime: Datetime del turno
        """
        try:
            hora_obj = datetime.strptime(self._hora, '%H:%M').time()
            return datetime.combine(self._fecha, hora_obj)
        except ValueError:
            return None
    
    def obtener_datos_candidato(self) -> dict:
        """
        Retorna datos del candidato de la evaluación asociada.
        
        Returns:
            dict: Datos del candidato
        """
        cand = self._evaluacion.candidato
        return {
            'id': cand.id,
            'nombre': cand.nombre,
            'email': cand.email,
            'telefono': cand.telefono
        }
    
    def obtener_datos_puesto(self) -> dict:
        """
        Retorna datos del puesto de la búsqueda asociada.
        
        Returns:
            dict: Datos del puesto
        """
        busq = self._evaluacion.busqueda
        return {
            'id': busq.id,
            'titulo': busq.titulo_puesto,
            'descripcion': busq.descripcion,
            'salario_rango': busq.obtener_rango_salario()
        }
    
    def obtener_info(self) -> str:
        """
        Retorna información detallada del turno.
        
        Returns:
            str: Información formateada
        """
        cand = self._evaluacion.candidato
        busq = self._evaluacion.busqueda
        
        info = f"""
        ═══════════════════════════════════════════
        TURNO DE ENTREVISTA
        ═══════════════════════════════════════════
        ID: {self._id}
        Candidato: {cand.nombre}
        Puesto: {busq.titulo_puesto}
        Fecha: {self._fecha.strftime('%d/%m/%Y')}
        Hora: {self._hora}
        Entrevistador: {self._entrevistador}
        Sala: {self._sala}
        Estado: {self._estado.value}
        Observaciones: {self._observaciones if self._observaciones else "Sin observaciones"}
        ═══════════════════════════════════════════
        """
        return info
    
    def obtener_info_compacta(self) -> dict:
        """
        Retorna información compacta en formato diccionario.
        
        Returns:
            dict: Información compacta
        """
        return {
            'id': self._id,
            'evaluacion_id': self._evaluacion.id,
            'candidato_nombre': self._evaluacion.candidato.nombre,
            'puesto': self._evaluacion.busqueda.titulo_puesto,
            'fecha': self._fecha.isoformat(),
            'hora': self._hora,
            'entrevistador': self._entrevistador,
            'sala': self._sala,
            'estado': self._estado.value,
            'observaciones': self._observaciones,
            'fecha_creacion': self._fecha_creacion.isoformat()
        }
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"Turno {self._id}: {self._evaluacion.candidato.nombre} - {self._fecha} {self._hora}"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"Turno(id={self._id}, evaluacion_id={self._evaluacion.id}, fecha={self._fecha}, hora={self._hora})"
