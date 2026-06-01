"""Clase Calendario - Gestiona disponibilidad de horarios y turnos"""
from datetime import datetime, time, timedelta, date
from typing import Dict, List


class Calendario:
    """Gestiona disponibilidad de horarios y turnos"""
    
    _contador_ids = 0
    
    def __init__(self, salas: List[str] = None):
        self._id = self._generar_id()
        self._horarios_disponibles: Dict[str, List[str]] = {}
        self._turnos = []
        self._salas = salas or ["Sala A", "Sala B", "Sala C"]
        self._fecha_inicio = date.today()
        self._fecha_fin = date.today() + timedelta(days=90)
        self._inicializar_horarios()
    
    @staticmethod
    def _generar_id() -> int:
        Calendario._contador_ids += 1
        return Calendario._contador_ids
    
    def _inicializar_horarios(self) -> None:
        fecha = self._fecha_inicio
        while fecha <= self._fecha_fin:
            if fecha.weekday() < 5:
                fecha_str = fecha.strftime('%Y-%m-%d')
                self._horarios_disponibles[fecha_str] = self._generar_horarios()
            fecha += timedelta(days=1)
    
    def _generar_horarios(self) -> List[str]:
        horarios = []
        inicio = datetime.combine(date.today(), time(9, 0))
        fin = datetime.combine(date.today(), time(17, 0))
        actual = inicio
        while actual <= fin:
            horarios.append(actual.strftime('%H:%M'))
            actual += timedelta(minutes=30)
        return horarios
    
    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def turnos(self) -> List:
        return self._turnos.copy()
    
    # Métodos
    def obtener_slots_libres(self, fecha: str) -> List[str]:
        if fecha not in self._horarios_disponibles:
            return []
        libres = self._horarios_disponibles[fecha].copy()
        for turno in self._turnos:
            if turno.fecha.strftime('%Y-%m-%d') == fecha and turno.hora in libres:
                libres.remove(turno.hora)
        return libres
    
    def esta_disponible(self, fecha: str, hora: str) -> bool:
        return hora in self.obtener_slots_libres(fecha)
    
    def agregar_turno(self, turno) -> bool:
        fecha_str = turno.fecha.strftime('%Y-%m-%d')
        if self.esta_disponible(fecha_str, turno.hora):
            self._turnos.append(turno)
            return True
        return False
    
    def eliminar_turno(self, turno) -> bool:
        if turno in self._turnos:
            self._turnos.remove(turno)
            return True
        return False
    
    def obtener_turnos_proximos(self, cantidad: int = 10) -> List:
        futuros = [t for t in self._turnos if t.fecha >= date.today()]
        ordenados = sorted(futuros, key=lambda x: (x.fecha, x.hora))
        return ordenados[:cantidad]
    
    def obtener_turnos_por_evaluacion(self, evaluacion_id: int) -> List:
        return [t for t in self._turnos if t.evaluacion.id == evaluacion_id]
    
    def obtener_todos_turnos(self) -> List:
        return sorted(self._turnos, key=lambda x: (x.fecha, x.hora))
    
    def __str__(self) -> str:
        return f"Calendario (ID: {self._id}, Turnos: {len(self._turnos)})"
