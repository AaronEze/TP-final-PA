from datetime import datetime, time, timedelta, date
from src.db import db
from src.models.turno import TurnoModel

class CalendarioService:
    
    @staticmethod
    def generar_horarios_base() -> list[str]:
        """Tu lógica original: genera bloques de 30 min entre las 09:00 y las 17:00"""
        horarios = []
        inicio = datetime.combine(date.today(), time(9, 0))
        fin = datetime.combine(date.today(), time(17, 0))
        actual = inicio
        while actual <= fin:
            horarios.append(actual.strftime('%H:%M'))
            actual += timedelta(minutes=30)
        return horarios

    @staticmethod
    def obtener_slots_libres(fecha_str: str) -> list[str]:
        """Busca qué horarios de tu lista base no están ocupados en la BD para esa fecha (ignora cancelados)"""
        try:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return []

        # 1. Traemos los horarios fijos de 9 a 17 
        libres = CalendarioService.generar_horarios_base()
        
        # 2. Consultamos a la base de datos qué turnos ya están tomados ese día y que NO estén cancelados
        turnos_ocupados = TurnoModel.query.filter(TurnoModel.fecha == fecha_obj, TurnoModel.estado != "cancelado").all()
        
        # 3. Removemos los horarios ocupados
        for turno in turnos_ocupados:
            if turno.hora in libres:
                libres.remove(turno.hora)
                
        return libres

    @staticmethod
    def agregar_turno(fecha_str: str, hora_str: str, entrevistador: str, sala: str, evaluacion_id: int) -> bool:
        """Valida disponibilidad usando tu lógica y persiste en SQL con todos tus campos reales"""
        # Chequeamos si el horario está disponible usando el método de arriba
        slots_libres = CalendarioService.obtener_slots_libres(fecha_str)
        
        if hora_str in slots_libres:
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            # Creamos el registro en la BD con todos los atributos correspondientes
            nuevo_turno = TurnoModel(
                fecha=fecha_obj, 
                hora=hora_str, 
                entrevistador=entrevistador,
                sala=sala,
                evaluacion_id=evaluacion_id
            )
            db.session.add(nuevo_turno)
            db.session.commit()
            return True
        return False

    @staticmethod
    def cancelar_turno(turno_id: int, motivo: str = "") -> bool:
        """Tu lógica original de cancelar: cambia el estado a cancelado e incluye el motivo si corresponde"""
        turno = TurnoModel.query.get(turno_id)
        if turno and turno.estado in ["agendado", "no_presentado"]:
            turno.estado = "cancelado"
            turno.observaciones = motivo
            db.session.commit()
            return True
        return False

    @staticmethod
    def completar_turno(turno_id: int, observaciones: str = "") -> bool:
        """Tu lógica original de completar: pasa el turno a completado y agrega las notas finales"""
        turno = TurnoModel.query.get(turno_id)
        if turno and turno.estado == "agendado":
            turno.estado = "completado"
            turno.observaciones = observaciones
            db.session.commit()
            return True
        return False

    @staticmethod
    def marcar_no_presentado(turno_id: int) -> bool:
        """Tu lógica original: marca que el candidato no asistió a la entrevista agendada"""
        turno = TurnoModel.query.get(turno_id)
        if turno and turno.estado == "agendado":
            turno.estado = "no_presentado"
            db.session.commit()
            return True
        return False

    @staticmethod
    def obtener_turnos_proximos(cantidad: int = 10) -> list:
        """Trae los turnos futuros ordenados desde SQL (tu método original mejorado)"""
        hoy = date.today()
        # Filtramos en SQL los turnos de hoy en adelante, ordenamos por fecha y hora, y limitamos la cantidad
        turnos = TurnoModel.query.filter(TurnoModel.fecha >= hoy)\
                                 .order_by(TurnoModel.fecha.asc(), TurnoModel.hora.asc())\
                                 .limit(cantidad).all()
        return [t.to_dict() for t in turnos]

    @staticmethod
    def eliminar_turno_por_id(turno_id: int) -> bool:
        """Tu lógica original de eliminar_turno: Busca en SQL por ID y lo remueve físicamente"""
        turno = TurnoModel.query.get(turno_id)
        if turno:
            db.session.delete(turno)
            db.session.commit()
            return True
        return False

    @staticmethod
    def obtener_turnos_por_evaluacion(evaluacion_id: int) -> list:
        """Tu lógica original: Filtra los turnos que correspondan a una evaluación específica"""
        turnos = TurnoModel.query.filter_by(evaluacion_id=evaluacion_id).all()
        return [t.to_dict() for t in turnos]

    @staticmethod
    def obtener_todos_turnos() -> list:
        """Tu lógica original: Trae absolutamente todos los turnos ordenados cronológicamente"""
        turnos = TurnoModel.query.order_by(TurnoModel.fecha.asc(), TurnoModel.hora.asc()).all()
        return [t.to_dict() for t in turnos]