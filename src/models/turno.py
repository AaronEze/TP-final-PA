from src.db import db
from datetime import datetime, date

class TurnoModel(db.Model):
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    entrevistador = db.Column(db.String(100), nullable=False)
    sala = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(20), default="agendado") # agendado, completado, cancelado, no_presentado
    observaciones = db.Column(db.Text, default="")
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)
    
    # Clave foránea que apunta a la evaluación
    evaluacion_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.id'), nullable=False)

    def es_futuro(self) -> bool:
        """Tu lógica original para verificar vigencia"""
        return self.fecha >= date.today()

    def obtener_datetime(self) -> datetime:
        """Tu lógica original para consolidar fecha y hora"""
        try:
            hora_obj = datetime.strptime(self.hora, '%H:%M').time()
            return datetime.combine(self.fecha, hora_obj)
        except ValueError:
            return None

    def to_dict(self):
        evaluacion = getattr(self, 'evaluacion', None)
        return {
            'id': self.id,
            'evaluacion_id': self.evaluacion_id,
            'candidato_nombre': evaluacion.candidato.nombre if evaluacion and getattr(evaluacion, 'candidato', None) else "Desconocido",
            'puesto': evaluacion.busqueda.titulo_puesto if evaluacion and getattr(evaluacion, 'busqueda', None) else "Desconocido",
            'fecha': self.fecha.isoformat(),
            'hora': self.hora,
            'entrevistador': self.entrevistador,
            'sala': self.sala,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion.isoformat()
        }