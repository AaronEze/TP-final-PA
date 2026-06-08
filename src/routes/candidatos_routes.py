from flask import Blueprint, jsonify, request
from src.services.sistema_service import SistemaService

# Creamos el Blueprint para candidatos
candidatos_bp = Blueprint('candidatos_bp', __name__)

# 1. Registrar Candidato (POST)
#  Al registrar el Blueprint, esto mapeará a /api/candidatos
@candidatos_bp.route('', methods=['POST'])
def registrar_candidato():
    data = request.get_json()
    
    if not data or 'nombre' not in data or 'email' not in data:
        return jsonify({"error": "Faltan datos obligatorios (nombre y email)"}), 400
        
    nuevo_cand = SistemaService.registrar_candidato(
        nombre=data['nombre'],
        email=data['email'],
        telefono=data.get('telefono', ''),
        anos_experiencia=int(data.get('anos_experiencia', 0)),
        cv=data.get('cv', '')
    )
    
    if nuevo_cand:
        if 'habilidades' in data and isinstance(data['habilidades'], list):
            SistemaService.agregar_habilidades_candidato(nuevo_cand.id, data['habilidades'])
            
        return jsonify({
            "mensaje": "Candidato registrado con éxito en la Base de Datos",
            "candidato": nuevo_cand.to_dict()
        }), 201
    else:
        return jsonify({"error": "No se pudo registrar. El email ya existe."}), 400

# 2. Listar Candidatos (GET)
@candidatos_bp.route('', methods=['GET'])
def listar_candidatos():
    candidatos = SistemaService.obtainer_todos_candidatos()
    return jsonify([c.to_dict() for c in candidatos]), 200