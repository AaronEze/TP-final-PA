from flask import Flask, jsonify, request
from main import SistemaEntrevistas

app = Flask(__name__)

sistema = SistemaEntrevistas()

# Endpoint de prueba para saber si la API está viva
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        "status": "online",
        "mensaje": "¡Hola! La API del Sistema de Turnos está funcionando",
        "materia": "Programación Avanzada"
    }), 200

# Endpoint para listar todos los candidatos (GET)
@app.route('/api/candidatos', methods=['GET'])
def obtener_candidatos():
    # Transformamos  objetos Candidato a diccionarios JSON usando el to_dict() 
    lista_json = [c.to_dict() for c in sistema._candidatos]
    return jsonify(lista_json), 200

if __name__ == '__main__':
    # Esto corre un servidor local para hacer pruebas
    app.run(debug=True, port=5000)