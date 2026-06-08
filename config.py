import os

class Config:
    # Si Render nos da una base de datos real, usa esa. 
    # Si no (caso local), crea un archivo llamado 'entrevistas.db'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///entrevistas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False