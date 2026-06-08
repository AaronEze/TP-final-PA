from src.db import db

class CandidatoModel(db.Model):
    __tablename__ = 'candidatos'

    # Definimos las columnas de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(50), nullable=True)
    anos_experiencia = db.Column(db.Integer, default=0)
    cv = db.Column(db.Text, nullable=True)
    
    # Guardamos las habilidades como un texto separado por comas para simplificarlo en la base de datos
    habilidades = db.Column(db.Text, nullable=True, default="")

    def to_dict(self):
        """Convierte el modelo a un diccionario idéntico al formato que usabas antes"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono or "",
            "anos_experiencia": self.anos_experiencia,
            "cv": self.cv or "",
            "habilidades": self.habilidades.split(",") if self.habilidades else []
        }