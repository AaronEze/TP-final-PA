from flask import Flask, jsonify, request
from main import SistemaEntrevistas
from candidato import EstadoCandidato

app = Flask(__name__)

# Inicializa el sistema global en memoria
sistema = SistemaEntrevistas()

# ENDPOINT DE PRUEBA 
@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({
        "status": "online",
        "mensaje": "¡Hola! La API del Sistema de Turnos está funcionando"
    }), 200


# ==========================================
# 📋 SECCIÓN: CANDIDATOS
# ==========================================

# 1. Registrar un Candidato nuevo (POST)
@app.route('/api/candidatos', methods=['POST'])
def registrar_candidato():
    data = request.get_json()
    
    # Validamos que vengan los datos obligatorios
    if not data or 'nombre' not in data or 'email' not in data:
        return jsonify({"error": "Faltan datos obligatorios (nombre y email)"}), 400
        
    # método del sistema original
    nuevo_cand = sistema.registrar_candidato(
        nombre=data['nombre'],
        email=data['email'],
        telefono=data.get('telefono', ''),
        anos_experiencia=int(data.get('anos_experiencia', 0)),
        cv=data.get('cv', '')
    )
    
    if nuevo_cand:
        # Si pasaron habilidades en la petición, se las agregam
        if 'habilidades' in data and isinstance(data['habilidades'], list):
            sistema.agregar_habilidades_candidato(nuevo_cand.id, data['habilidades'])
            
        return jsonify({
            "mensaje": "Candidato registrado con éxito",
            "candidato": nuevo_cand.to_dict()
        }), 201
    else:
        return jsonify({"error": "No se pudo registrar el candidato (Email o teléfono inválidos)"}), 400

# 2. Listar todos los Candidatos (GET)
@app.route('/api/candidatos', methods=['GET'])
def listar_candidatos():
    # Convertir la lista de objetos a diccionarios JSON
    candidatos_json = [c.to_dict() for c in sistema._candidatos]
    return jsonify(candidatos_json), 200



#SECCION: BUSQUEDAS (VACANTES)


# 3. Crear una nueva Búsqueda laboral (POST)
@app.route('/api/busquedas', methods=['POST'])
def crear_busqueda():
    data = request.get_json()
    
    if not data or 'titulo' not in data or 'exp_min' not in data:
        return jsonify({"error": "Faltan datos obligatorios (titulo y exp_min)"}), 400
        
    nueva_busq = sistema.crear_busqueda(
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        salario_min=float(data.get('salario_min', 0.0)),
        salario_max=float(data.get('salario_max', 0.0)),
        skills=data.get('skills', []),
        exp_min=int(data['exp_min'])
    )
    
    return jsonify({
        "mensaje": "Búsqueda de empleo creada con éxito",
        "busqueda": nueva_busq.to_dict()
    }), 201

# 4. Listar todas las Búsquedas (GET)
@app.route('/api/busquedas', methods=['GET'])
def listar_busquedas():
    busquedas_json = [b.to_dict() for b in sistema._busquedas]
    return jsonify(busquedas_json), 200


# ==========================================
# 📊 SECCIÓN: EVALUACIONES
# ==========================================

# 5. Evaluar un Candidato (POST)
@app.route('/api/evaluaciones', methods=['POST'])
def evaluar_candidato():
    data = request.get_json()
    
    # Validamos datos mínimos requeridos
    if not data or 'candidato_id' not in data or 'busqueda_id' not in data or 'resultado' not in data:
        return jsonify({"error": "Faltan datos obligatorios (candidato_id, busqueda_id y resultado)"}), 400
        
    evaluacion = sistema.evaluar_candidato(
        candidato_id=int(data['candidato_id']),
        busqueda_id=int(data['busqueda_id']),
        evaluador=data.get('evaluador', 'Recruiter Anonymous'),
        resultado=data['resultado'], # "aprobado" o "rechazado"
        puntuacion=float(data.get('puntuacion', 0.0)),
        comentarios=data.get('comentarios', '')
    )
    
    if evaluacion:
        return jsonify({
            "mensaje": "Evaluación registrada con éxito",
            "evaluacion": evaluacion.to_dict()
        }), 201
    else:
        return jsonify({"error": "No se pudo registrar la evaluación. Verificá los IDs."}), 400



# SECCION: CALENDARIO Y TURNOS


# 6. Ver slots disponibles para una fecha (GET)
# Ejemplo de uso: /api/calendario/disponibilidad?fecha=2026-06-15
@app.route('/api/calendario/disponibilidad', methods=['GET'])
def ver_disponibilidad():
    # Capturamos la fecha que viene en la URL como parámetro
    fecha_str = request.args.get('fecha')
    
    if not fecha_str:
        return jsonify({"error": "Falta el parámetro 'fecha' en formato YYYY-MM-DD"}), 400
        
    slots_libres = sistema.obtener_slots_disponibles(fecha_str)
    
    return jsonify({
        "fecha": fecha_str,
        "slots_disponibles": slots_libres
    }), 200


# 7. Agendar un Turno de entrevista (POST)
@app.route('/api/turnos', methods=['POST'])
def agendar_turno():
    data = request.get_json()
    
    required = ['evaluacion_id', 'fecha', 'hora', 'entrevistador']
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Faltan datos obligatorios. Requeridos: {required}"}), 400
        
    nuevo_turno = sistema.agendar_turno(
        evaluacion_id=int(data['evaluacion_id']),
        fecha=data['fecha'], # YYYY-MM-DD
        hora=data['hora'],   # HH:MM
        entrevistador=data['entrevistador'],
        sala=data.get('sala', 'Virtual Room')
    )
    
    if nuevo_turno:
        return jsonify({
            "mensaje": "Turno agendado con éxito",
            "turno": nuevo_turno.to_dict()
        }), 201
    else:
        return jsonify({"error": "No se pudo agendar el turno. Horario no disponible o evaluación inexistente."}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)