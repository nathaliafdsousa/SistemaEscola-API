from flask import Blueprint, request, jsonify
from Models.Nota import Nota, db
import requests

notatividade_bp = Blueprint("notatividade_bp", __name__)

GERENCIAMENTO_URL = "http://localhost:5000"

@notatividade_bp.route("/notas", methods=["POST"])
def criar_nota():
    data = request.json
    r_atividade = requests.get(f"{GERENCIAMENTO_URL}/atividades/{data['atividade_id']}")
    if r_atividade.status_code != 200:
        return jsonify({"erro":"Atividade não encontrada"}), 400
    
    nota = Nota(**data)
    db.session.add(nota)
    db.session.commit()

    return jsonify({"message":"Nota criada com sucesso"}), 201

@notatividade_bp.route("/notas", methods=["GET"])
def listar_notas():
    notas = Nota.query.all()

    if not notas:
        return jsonify({"erro":"Nenhuma nota encontrada"}), 404
    return jsonify([nt.to_dict() for nt in notas]), 200

@notatividade_bp.route("/notas/<int:id>", methods=["GET"])
def obter_nota(id):
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro":"Nota não encontrada"}), 404
    return jsonify(nota.to_dict()),200

@notatividade_bp.route("/notas/<int:id>", methods=["PUT"])
def atualizar_nota(id):
    data = request.json
    nota = Nota.query.get(id)

    if not nota:
        return jsonify({"erro":"Nota não encontrada"}), 404
    
    if "atividade_id" in data:
        r_atividade = requests.get(f"{GERENCIAMENTO_URL}/atividades/{data['atividade_id']}")
        if r_atividade.status_code != 200:
            return jsonify({"erro":"Atividade não encontrada"}), 400
        nota.atividade_id = data["atividade_id"]