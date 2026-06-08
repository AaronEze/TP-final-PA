from flask import Blueprint, jsonify, request
from src.services.sistema_service import SistemaService

busquedas_bp = Blueprint('busquedas_bp', __name__)

# 3. Crear una nueva Búsqueda (POST)
@busquedas_bp.route('', methods=['POST'])
def crear_busqueda():
    data = request.get_json()
    
    if not data or 'titulo' not in data or 'exp_min' not in data:
        return jsonify({"error": "Faltan datos obligatorios (titulo y exp_min)"}), 400
        
    nueva_busq = SistemaService.crear_busqueda(
        titulo=data['titulo'],
        descripcion=data.get('descripcion', ''),
        salario_min=float(data.get('salario_min', 0.0)),
        salario_max=float(data.get('salario_max', 0.0)),
        skills=data.get('skills', []),
        exp_min=int(data['exp_min'])
    )
    
    return jsonify({
        "mensaje": "Búsqueda de empleo guardada con éxito en la Base de Datos",
        "busqueda": nueva_busq.to_dict()
    }), 201

# 4. Listar todas las Búsquedas (GET)
@busquedas_bp.route('', methods=['GET'])
def listar_busquedas():
    busquedas = SistemaService.obtener_todas_busquedas()
    return jsonify([b.to_dict() for b in busquedas]), 200