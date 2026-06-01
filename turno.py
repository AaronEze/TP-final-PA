"""Clase Turno - Entrevista agendada simplificada"""
from datetime import date, datetime
from enum import Enum


class EstadoTurno(Enum):
    AGENDADO = "agendado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"
    NO_PRESENTADO = "no_presentado"


class Turno:
    """Entrevista agendada"""
    
    _contador_ids = 0
    
    def __init__(self, evaluacion, fecha: date, hora: str, 
                 entrevistador: str, sala: str):
        self._id = self._generar_id()
        self._evaluacion = evaluacion
        self._fecha = fecha
        self._hora = hora
        self._entrevistador = entrevistador
        self._sala = sala
        self._estado = EstadoTurno.AGENDADO
        self._observaciones = ""
        self._fecha_creacion = datetime.now()
    
    @staticmethod
    def _generar_id() -> int:
        Turno._contador_ids += 1
        return Turno._contador_ids
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def evaluacion(self):
        return self._evaluacion
    
    @property
    def fecha(self) -> date:
        return self._fecha
    
    @property
    def hora(self) -> str:
        return self._hora
    
    @property
    def entrevistador(self) -> str:
        return self._entrevistador
    
    @property
    def sala(self) -> str:
        return self._sala
    
    @property
    def estado(self) -> EstadoTurno:
        return self._estado
    
    @property
    def observaciones(self) -> str:
        return self._observaciones
    
    # Métodos
    def cancelar(self, motivo: str = "") -> bool:
        if self._estado in [EstadoTurno.COMPLETADO, EstadoTurno.CANCELADO]:
            return False
        self._estado = EstadoTurno.CANCELADO
        self._observaciones = motivo
        return True
    
    def completar(self, observaciones: str = "") -> bool:
        if self._estado != EstadoTurno.AGENDADO:
            return False
        self._estado = EstadoTurno.COMPLETADO
        self._observaciones = observaciones
        return True
    
    def marcar_no_presentado(self) -> bool:
        if self._estado != EstadoTurno.AGENDADO:
            return False
        self._estado = EstadoTurno.NO_PRESENTADO
        return True
    
    def es_futuro(self) -> bool:
        return self._fecha >= date.today()
    
    def obtener_datetime(self) -> datetime:
        try:
            hora_obj = datetime.strptime(self._hora, '%H:%M').time()
            return datetime.combine(self._fecha, hora_obj)
        except ValueError:
            return None
    
    def to_dict(self) -> dict:
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
        return f"Turno {self._id}: {self._evaluacion.candidato.nombre} - {self._fecha} {self._hora}"
