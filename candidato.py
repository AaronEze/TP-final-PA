"""Clase Candidato - Herencia simplificada"""
from datetime import datetime
from enum import Enum
from validaciones import validar_email


class EstadoCandidato(Enum):
    REGISTRADO = "registrado"
    EVALUADO = "evaluado"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


class Candidato:
    """Representa un candidato en el sistema"""
    
    _contador_ids = 0
    
    def __init__(self, nombre: str, email: str, telefono: str, 
                 anos_experiencia: int, cv: str):
        if not validar_email(email):
            raise ValueError(f"Email inválido: {email}")
        if anos_experiencia < 0:
            raise ValueError("Años no pueden ser negativos")
            
        self._id = self._generar_id()
        self._nombre = nombre
        self._email = email
        self._telefono = telefono
        self._anos_experiencia = anos_experiencia
        self._cv = cv
        self._habilidades = []
        self._estado = EstadoCandidato.REGISTRADO
        self._fecha_registro = datetime.now()
    
    @staticmethod
    def _generar_id() -> int:
        Candidato._contador_ids += 1
        return Candidato._contador_ids
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    @property
    def anos_experiencia(self) -> int:
        return self._anos_experiencia
    
    @property
    def habilidades(self) -> list:
        return self._habilidades.copy()
    
    @property
    def cv(self) -> str:
        return self._cv
    
    @property
    def estado(self) -> EstadoCandidato:
        return self._estado
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoCandidato):
        self._estado = nuevo_estado
    
    # Métodos
    def agregar_habilidad(self, habilidad: str) -> None:
        if habilidad and habilidad not in self._habilidades:
            self._habilidades.append(habilidad)
    
    def agregar_multiples_habilidades(self, habilidades: list) -> None:
        for h in habilidades:
            self.agregar_habilidad(h)
    
    def tiene_experiencia_minima(self, anos: int) -> bool:
        return self._anos_experiencia >= anos
    
    def tiene_habilidad(self, habilidad: str) -> bool:
        return habilidad.lower() in [h.lower() for h in self._habilidades]
    
    def tiene_todas_habilidades(self, habilidades: list) -> bool:
        return all(self.tiene_habilidad(h) for h in habilidades)
    
    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'nombre': self._nombre,
            'email': self._email,
            'telefono': self._telefono,
            'anos_experiencia': self._anos_experiencia,
            'habilidades': self._habilidades.copy(),
            'estado': self._estado.value,
            'fecha_registro': self._fecha_registro.isoformat()
        }
    
    def __str__(self) -> str:
        return f"{self._nombre} ({self._anos_experiencia} años, {self._estado.value})"
