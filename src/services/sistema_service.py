from src.db import db
from src.models.candidato import CandidatoModel
from src.models.busqueda import BusquedaModel

class SistemaService:
    
    # OPERACIONES DE CANDIDATOS 
    
    @staticmethod
    def registrar_candidato(nombre, email, telefono="", anos_experiencia=0, cv=""):
        # Verificamos si ya existe un candidato con ese email para evitar duplicados
        existe = CandidatoModel.query.filter_by(email=email).first()
        if existe:
            return None # Devolvemos None si el email ya está registrado
            
        nuevo_candidato = CandidatoModel(
            nombre=nombre,
            email=email,
            telefono=telefono,
            anos_experiencia=anos_experiencia,
            cv=cv
        )
        
        db.session.add(nuevo_candidato)
        db.session.commit() # Guarda el candidato en la base de datos relacional
        return nuevo_candidato

    @staticmethod
    def obtener_todos_candidatos():
        # Hace un 'SELECT * FROM candidatos' automáticamente
        return CandidatoModel.query.all()

    @staticmethod
    def agregar_habilidades_candidato(candidato_id, lista_habilidades):
        candidato = CandidatoModel.query.get(candidato_id)
        if candidato:
            # Unimos la lista con comas para guardarla en la celda de texto de SQL
            texto_habilidades = ",".join(lista_habilidades)
            candidato.habilidades = texto_habilidades
            db.session.commit()
            return True
        return False


    #  OPERACIONES DE BÚSQUEDAS 

    @staticmethod
    def crear_busqueda(titulo, descripcion="", salario_min=0.0, salario_max=0.0, skills=None, exp_min=0):
        if skills is None:
            skills = []
            
        texto_skills = ",".join(skills)
        
        nueva_busqueda = BusquedaModel(
            titulo=titulo,
            descripcion=descripcion,
            salario_min=salario_min,
            salario_max=salario_max,
            exp_min=exp_min,
            skills=texto_skills
        )
        
        db.session.add(nueva_busqueda)
        db.session.commit()
        return nueva_busqueda

    @staticmethod
    def obtener_todas_busquedas():
        return BusquedaModel.query.all()