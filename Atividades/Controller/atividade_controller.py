from flask import Blueprint, request, jsonify
from Models.Atividade import Atividade, db
import requests

atividade_bp = Blueprint("atividade_bp", __name__)

GERENCIAMENTO_URL = "http://localhost:5000"  # serviço de gerenciamento

atividade_bp.route("/atividades", methods=["POST"])
def criar_atividade():
    data = request.json
    r_turma = requests.get(f"{GERENCIAMENTO_URL}/turmas/{data['turma_id']}")
    if r_turma.status_code != 200:
        return jsonify({"erro": "Turma não encontrada"}), 400
    
    r_prof = requests.get(f"{GERENCIAMENTO_URL}/professores/{data['professor_id']}")
    if r_prof.status_code != 200:
        return jsonify({"erro": "Professor não encontrado"}), 400
    
    atividade = Atividade(**data)
    db.session.add(atividade)
    db.session.commit()

    return jsonify({"message": "Atividade criada com sucesso"}), 201

@atividade_bp.route("/atividades", methods=["GET"])
def listar_atividades():
    atividades = Atividade.query.all()
    if not atividades:
        return jsonify({"mensagem": "Nenhuma atividade encontrada"}), 404
    return jsonify([atv.to_dict() for atv in atividades]), 200

@atividade_bp.route("/atividades/<int:id>", methods=["GET"])
def obter_atividade(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404
    return jsonify(atividade.to_dict()),200

@atividade_bp.route("/atividades/<int:id>", methods=["PUT"])
def atualizar_atividade(id):
    data = request.json
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}),404
    
    if "turma_id" in data:
        r_turma = requests.get(f"{GERENCIAMENTO_URL}/turmas/{data['turma_id']}")
        if r_turma.status_code != 200:
            return jsonify({"erro": "Turma não encontrada"}), 400
        atividade.turma_id = data["turma_id"]
    
    if "professor_id" in data:
        r_prof = requests.get(f"{GERENCIAMENTO_URL}/professores/{data['professor_id']}")
        if r_prof.status_code != 200:
            return jsonify({"erro": "Professor não encontrado"}), 400
        atividade.professor_id = data["professor_id"]

        atividade.nome_atividade = data.get("nome_atividade", atividade.nome_atividade)
        atividade.descricao = data.get("descricao", atividade.descricao)
        atividade.peso_porcento = data.get("peso_porcento", atividade.peso_porcento)
        atividade.data_entrega = data.get("data_entrega", atividade.data_entrega)
        
        db.session.commit()
        return jsonify(f"Atividade atualizada com sucesso: {atividade.to_dict()}"),200

@atividade_bp.route("/atividades/<int:id>", methods=["DELETE"])
def deletar_atividade(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro":"Atividade não encontrada"}), 404
    
    db.session.delete(atividade)
    db.session.commit()

    return jsonify({"mensagem": "Atividade deletada com sucesso"}), 200








