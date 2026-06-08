from src.db import db

class BusquedaModel(db.Model):
    __tablename__ = 'busquedas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    salario_min = db.Column(db.Float, default=0.0)
    salario_max = db.Column(db.Float, default=0.0)
    exp_min = db.Column(db.Integer, nullable=False, default=0)
    
    # guardamos las skills requeridas separadas por comas
    skills = db.Column(db.Text, nullable=True, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion or "",
            "salario_min": self.salario_min,
            "salario_max": self.salario_max,
            "exp_min": self.exp_min,
            "skills": self.skills.split(",") if self.skills else []
        }