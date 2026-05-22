"""
Módulo: models/calendario.py
Clase Calendario - Gestiona disponibilidad de horarios y turnos (AGREGACIÓN)
"""

from datetime import datetime, time, timedelta, date
from typing import Dict, List, Tuple


class Calendario:
    """
    Clase Calendario que gestiona la disponibilidad de horarios y turnos.
    Ejemplo de AGREGACIÓN: contiene una colección de Turnos.
    
    Attributes:
        _id (int): Identificador único
        _horarios_disponibles (Dict): Diccionario con horarios disponibles por fecha
        _turnos_agendados (List): Lista de turnos agendados [AGREGACIÓN]
        _salas_disponibles (List[str]): Lista de salas disponibles
        _fecha_inicio_calendario (date): Fecha inicial del calendario
        _fecha_fin_calendario (date): Fecha final del calendario
    """
    
    _contador_ids = 0
    
    def __init__(self, salas_disponibles: List[str] = None):
        """
        Constructor de Calendario.
        
        Args:
            salas_disponibles (List[str]): Lista de salas disponibles para entrevistas
        """
        self._id = self._generar_id()
        self._horarios_disponibles: Dict[str, List[str]] = {}
        self._turnos_agendados: List = []  # AGREGACIÓN - Lista de Turnos
        self._salas_disponibles = salas_disponibles or ["Sala A", "Sala B", "Sala C"]
        self._fecha_inicio_calendario = date.today()
        self._fecha_fin_calendario = date.today() + timedelta(days=90)
        
        # Inicializar horarios disponibles para los próximos 90 días
        self._inicializar_horarios()
    
    @staticmethod
    def _generar_id() -> int:
        """Genera un ID único."""
        Calendario._contador_ids += 1
        return Calendario._contador_ids
    
    def _inicializar_horarios(self) -> None:
        """
        Inicializa los horarios disponibles para cada día (de lunes a viernes, 09:00 a 17:00).
        """
        fecha_actual = self._fecha_inicio_calendario
        
        while fecha_actual <= self._fecha_fin_calendario:
            # Solo agregar horarios para días de semana (0-4 = lunes a viernes)
            if fecha_actual.weekday() < 5:  # 0=lunes, 4=viernes
                fecha_str = fecha_actual.strftime('%Y-%m-%d')
                horarios = self._generar_slots_horarios()
                self._horarios_disponibles[fecha_str] = horarios
            
            fecha_actual += timedelta(days=1)
    
    def _generar_slots_horarios(self) -> List[str]:
        """
        Genera los slots horarios disponibles en un día (09:00 a 17:00 cada 30 min).
        
        Returns:
            List[str]: Lista de horarios disponibles
        """
        horarios = []
        hora_inicio = time(9, 0)
        hora_fin = time(17, 0)
        
        hora_actual = datetime.combine(date.today(), hora_inicio)
        hora_fin_obj = datetime.combine(date.today(), hora_fin)
        
        while hora_actual <= hora_fin_obj:
            horarios.append(hora_actual.strftime('%H:%M'))
            hora_actual += timedelta(minutes=30)
        
        return horarios
    
    # ============ GETTERS ============
    
    @property
    def id(self) -> int:
        """Retorna el ID del calendario."""
        return self._id
    
    @property
    def turnos_agendados(self) -> List:
        """Retorna la lista de turnos agendados."""
        return self._turnos_agendados.copy()
    
    @property
    def salas_disponibles(self) -> List[str]:
        """Retorna la lista de salas disponibles."""
        return self._salas_disponibles.copy()
    
    # ============ MÉTODOS DE DISPONIBILIDAD ============
    
    def obtener_slots_libres(self, fecha: str) -> List[str]:
        """
        Obtiene los slots horarios libres para una fecha específica.
        
        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'
            
        Returns:
            List[str]: Lista de horarios disponibles
        """
        if fecha not in self._horarios_disponibles:
            return []
        
        horarios_libres = self._horarios_disponibles[fecha].copy()
        
        # Filtrar los horarios que ya tienen turnos agendados
        for turno in self._turnos_agendados:
            if turno.fecha.strftime('%Y-%m-%d') == fecha:
                if turno.hora in horarios_libres:
                    horarios_libres.remove(turno.hora)
        
        return horarios_libres
    
    def esta_disponible(self, fecha: str, hora: str) -> bool:
        """
        Verifica si un slot específico está disponible.
        
        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'
            hora (str): Hora en formato 'HH:MM'
            
        Returns:
            bool: True si está disponible
        """
        return hora in self.obtener_slots_libres(fecha)
    
    def reservar_slot(self, fecha: str, hora: str) -> bool:
        """
        Reserva un slot horario.
        
        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'
            hora (str): Hora en formato 'HH:MM'
            
        Returns:
            bool: True si se reservó, False si ya estaba ocupado
        """
        if self.esta_disponible(fecha, hora):
            return True
        return False
    
    def liberar_slot(self, fecha: str, hora: str) -> None:
        """
        Libera un slot horario (cuando se cancela un turno).
        
        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'
            hora (str): Hora en formato 'HH:MM'
        """
        # Los turnos se eliminan de la lista cuando se cancelan
        pass
    
    def agregar_turno(self, turno) -> bool:
        """
        Agrega un turno al calendario [AGREGACIÓN].
        
        Args:
            turno (Turno): Turno a agregar
            
        Returns:
            bool: True si se agregó correctamente
        """
        fecha_str = turno.fecha.strftime('%Y-%m-%d')
        
        if self.esta_disponible(fecha_str, turno.hora):
            self._turnos_agendados.append(turno)
            return True
        return False
    
    def eliminar_turno(self, turno) -> bool:
        """
        Elimina un turno del calendario (cuando se cancela).
        
        Args:
            turno (Turno): Turno a eliminar
            
        Returns:
            bool: True si se eliminó
        """
        if turno in self._turnos_agendados:
            self._turnos_agendados.remove(turno)
            return True
        return False
    
    def obtener_turnos_del_dia(self, fecha: str) -> List:
        """
        Obtiene todos los turnos agendados para un día específico.
        
        Args:
            fecha (str): Fecha en formato 'YYYY-MM-DD'
            
        Returns:
            List: Lista de turnos del día
        """
        turnos_dia = [t for t in self._turnos_agendados 
                     if t.fecha.strftime('%Y-%m-%d') == fecha]
        return sorted(turnos_dia, key=lambda x: x.hora)
    
    def obtener_turnos_proximos(self, cantidad: int = 10) -> List:
        """
        Obtiene los próximos turnos agendados.
        
        Args:
            cantidad (int): Cantidad de turnos a retornar
            
        Returns:
            List: Lista de próximos turnos
        """
        turnos_futuros = [t for t in self._turnos_agendados 
                         if t.fecha >= date.today()]
        turnos_ordenados = sorted(turnos_futuros, key=lambda x: (x.fecha, x.hora))
        return turnos_ordenados[:cantidad]
    
    def obtener_turnos_por_evaluacion(self, evaluacion_id: int) -> List:
        """
        Obtiene todos los turnos asociados a una evaluación.
        
        Args:
            evaluacion_id (int): ID de la evaluación
            
        Returns:
            List: Lista de turnos
        """
        return [t for t in self._turnos_agendados 
               if t.evaluacion.id == evaluacion_id]
    
    # ============ MÉTODOS DE INFORMACIÓN ============
    
    def obtener_info(self) -> str:
        """
        Retorna información del calendario.
        
        Returns:
            str: Información formateada
        """
        info = f"""
        ═══════════════════════════════════════════
        CALENDARIO
        ═══════════════════════════════════════════
        ID: {self._id}
        Período: {self._fecha_inicio_calendario} a {self._fecha_fin_calendario}
        Salas disponibles: {', '.join(self._salas_disponibles)}
        Turnos agendados: {len(self._turnos_agendados)}
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
            'periodo_inicio': self._fecha_inicio_calendario.isoformat(),
            'periodo_fin': self._fecha_fin_calendario.isoformat(),
            'salas': self._salas_disponibles.copy(),
            'turnos_agendados': len(self._turnos_agendados),
            'proximos_turnos': len(self.obtener_turnos_proximos())
        }
    
    def __str__(self) -> str:
        """Representación en string."""
        return f"Calendario (ID: {self._id}, Turnos: {len(self._turnos_agendados)})"
    
    def __repr__(self) -> str:
        """Representación técnica."""
        return f"Calendario(id={self._id}, turnos={len(self._turnos_agendados)})"
