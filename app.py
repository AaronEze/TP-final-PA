from flask import Flask, jsonify
from config import Config
from src.db import db

# Importamos los Blueprints de las rutas
from src.routes.candidatos_routes import candidatos_bp
from src.routes.busquedas_routes import busquedas_bp

def create_app():
    app = Flask(__name__)
    
    # Cargamos la configuración (sabe si usa SQLite local o Postgres en Render)
    app.config.from_object(Config)
    
    # Inicializamos la base de datos con la app de Flask
    db.init_app(app)
    
    # Registramos los Blueprints definiendo su prefijo de URL
    app.register_blueprint(candidatos_bp, url_prefix='/api/candidatos')
    app.register_blueprint(busquedas_bp, url_prefix='/api/busquedas')
    
    # Endpoint global de prueba (Ping)
    @app.route('/api/ping', methods=['GET'])
    def ping():
        return jsonify({
            "status": "online",
            "mensaje": "¡Hola! La API con Base de Datos SQL está funcionando de diez"
        }), 200

    # Creamos las tablas en la base de datos de forma automática antes de arrancar
    with app.app_context():
        db.create_all()
        
    return app

# Creamos la instancia global para que Gunicorn pueda usarla, y también para correrla localmente con python app.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)