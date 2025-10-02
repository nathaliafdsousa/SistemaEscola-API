from flask import request, jsonify
from datetime import datetime
from Models import db, Turma 
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
turmas_bp = Blueprint("turmas", __name__)

turmas_bp.route("/turmas", methods=["POST"])
def criar_turma():
    try:
        data = request.get_json()

        nome = data.get("nome")
        ano = data.get("ano")
        professor_id = data.get("professor_id")

        nova_turma = Turma(nome=nome, ano=ano, professor_id=professor_id)
        db.session.add(nova_turma)
        db.session.commit()

        return jsonify({"message": "Turma criada com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar turma. Verifique os dados fornecidos."}), 400
    
@turmas_bp.route("/turmas", methods=["GET"])
def listar_turmas():
    turmas = Turma.query.all()
    resultado = []
    for turma in turmas:
        resultado.append({
            "id": turma.id,
            "nome": turma.nome,
            "ano": turma.ano,
            "professor_id": turma.professor_id
        })
    return jsonify(resultado), 200

@turmas_bp.route("/turmas/<int:turma_id>", methods=["GET"])
def obter_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 400

    resultado = {
        "id": turma.id,
        "nome": turma.nome,
        "ano": turma.ano,
        "professor_id": turma.professor_id
    }
    return jsonify(resultado), 200

@turmas_bp.route("/turmas/<int:turma_id>", methods=["PUT"])
def atualizar_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 400

    data = request.get_json()
    turma.nome = data.get("nome", turma.nome)
    turma.ano = data.get("ano", turma.ano)
    turma.professor_id = data.get("professor_id", turma.professor_id)

    db.session.commit()
    return jsonify({"message": "Turma atualizada com sucesso!"}), 200

@turmas_bp.route("/turmas/<int:turma_id>", methods=["DELETE"])
def deletar_turma(turma_id):
    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 400

    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma deletada com sucesso!"}), 200