from flask import Blueprint, request, jsonify
from models import Technology, db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_technologies = Blueprint('technologies', __name__)

@bp_technologies.route('/technologies', methods=['GET'])
@jwt_required()
def get_technologies():
    technologies = Technology.query.all()

    # Serializar cada tecnología en la lista
    serialized_technologies = [technology.serialize() for technology in technologies]

    return jsonify({"status": "success", "technologies": serialized_technologies}), 200

@bp_technologies.route('/technologies', methods=['POST'])
@jwt_required()
def new_technology():
    data = request.json
    technology_name = data.get('name')
    
    if not technology_name:
        return jsonify({"status": "error", "message": "El nombre de la tecnología es requerido"}), 400

    existing_technology = Technology.query.filter_by(name=technology_name).first()
    if existing_technology:
        return jsonify({"status": "error", "message": "La tecnología ya existe"}), 400

    new_technology = Technology(name=technology_name)

    try:
        # Insertar en la base de datos
        db.session.add(new_technology)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "technology": new_technology.serialize()}), 201
