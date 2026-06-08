from datetime import datetime
from src.db import db
from src.models.evaluacion import EvaluacionModel

class EvaluacionService:

    @staticmethod
    def crear_evaluacion(candidato_id: int, busqueda_id: int, evaluador: str) -> EvaluacionModel:
        """Crea un registro de evaluación en estado pendiente"""
        nueva_evaluacion = EvaluacionModel(candidato_id=candidato_id, busqueda_id=busqueda_id, evaluador=evaluador)
        db.session.add(nueva_evaluacion)
        db.session.commit()
        return nueva_evaluacion

    @staticmethod
    def evaluar_candidato(evaluacion_id: int, resultado: str, puntuacion: float, comentarios: str = "") -> bool:
        """Tu lógica operativa original de evaluar(): Valida rangos, strings y persiste en SQL"""
        if not (0 <= puntuacion <= 100):
            raise ValueError("Puntuación debe estar entre 0 y 100")
            
        evaluacion = EvaluacionModel.query.get(evaluacion_id)
        if not evaluacion:
            return False

        resultado_lower = resultado.lower()
        if resultado_lower == "aprobado":
            evaluacion.resultado = "aprobado"
        elif resultado_lower == "rechazado":
            evaluacion.resultado = "rechazado"
        else:
            raise ValueError("Resultado debe ser 'aprobado' o 'rechazado'")
            
        evaluacion.puntuacion = puntuacion
        evaluacion.comentarios = comentarios
        evaluacion.fecha_evaluacion = datetime.now()
        
        db.session.commit()
        return True