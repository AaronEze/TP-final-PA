from src.db import db
from datetime import datetime

class EvaluacionModel(db.Model):
    __tablename__ = 'evaluaciones'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluador = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.String(20), default="pendiente") # pendiente, aprobado, rechazado
    puntuacion = db.Column(db.Float, default=0.0)
    comentarios = db.Column(db.Text, default="")
    fecha_evaluacion = db.Column(db.DateTime, nullable=True)

    # Claves foráneas reales
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidatos.id'), nullable=False)
    busqueda_id = db.Column(db.Integer, db.ForeignKey('busquedas.id'), nullable=False)

    # Relaciones SQLAlchemy
    candidato = db.relationship('CandidatoModel', backref='evaluaciones')
    busqueda = db.relationship('BusquedaModel', backref='evaluaciones')
    turnos = db.relationship('TurnoModel', backref='evaluacion', cascade="all, delete-orphan")

    def es_aprobado(self) -> bool:
        return self.resultado == "aprobado"
    
    def es_rechazado(self) -> bool:
        return self.resultado == "rechazado"
    
    def esta_pendiente(self) -> bool:
        return self.resultado == "pendiente"

    def obtener_analisis(self) -> dict:
        analisis = self.busqueda.candidato_cumple_requisitos(self.candidato)
        return {
            'candidato_nombre': self.candidato.nombre,
            'puesto': self.busqueda.titulo_puesto,
            'resultado': self.resultado,
            'puntuacion': self.puntuacion,
            'cumple_requisitos': analisis['cumple_todos'],
            'cumple_experiencia': analisis['cumple_experiencia'],
            'cumple_skills': analisis['cumple_skills'],
            'skills_faltantes': analisis['skills_faltantes'],
            'comentarios': self.comentarios,
            'evaluador': self.evaluador,
            'fecha': self.fecha_evaluacion.strftime('%d/%m/%Y %H:%M') if self.fecha_evaluacion else "Pendiente"
        }

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'candidato_id': self.candidato_id,
            'candidato_nombre': self.candidato.nombre if self.candidato else "Desconocido",
            'busqueda_id': self.busqueda_id,
            'puesto': self.busqueda.titulo_puesto if self.busqueda else "Desconocido",
            'evaluador': self.evaluador,
            'resultado': self.resultado,
            'puntuacion': self.puntuacion,
            'comentarios': self.comentarios,
            'fecha_evaluacion': self.fecha_evaluacion.isoformat() if self.fecha_evaluacion else None
        }