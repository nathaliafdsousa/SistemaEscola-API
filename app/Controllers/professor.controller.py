from flask import request, jsonify
from datetime import datetime
from Models import db, Professor  
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
professores_bp = Blueprint("professores", __name__)

@professores_bp.route("/professores", methods=["POST"])
def criar_professor():
    try:
        data = request.get_json()

        nome = data.get("nome")
        idade = data.get("idade")
        disciplina = data.get("disciplina")

        novo_professor = Professor(nome=nome, idade=idade, disciplina=disciplina)
        db.session.add(novo_professor)
        db.session.commit()

        return jsonify({"message": "Professor criado com sucesso!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar professor. Verifique os dados fornecidos."}), 400
    
@professores_bp.route("/professores", methods=["GET"])
def listar_professores():
    professores = Professor.query.all()
    resultado = []
    for professor in professores:
        resultado.append({
            "id": professor.id,
            "nome": professor.nome,
            "idade": professor.idade,
            "disciplina": professor.disciplina
        })
    return jsonify(resultado), 200

@professores_bp.route("/professores/<int:professor_id>", methods=["GET"])
def obter_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({"error": "Professor não encontrado."}), 404

    resultado = {
        "id": professor.id,
        "nome": professor.nome,
        "idade": professor.idade,
        "disciplina": professor.disciplina
    }
    return jsonify(resultado), 200

@professores_bp.route("/professores/<int:professor_id>", methods=["PUT"])
def atualizar_professor(professor_id):
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({"error": "Professor não encontrado."}), 404

    data = request.get_json()
    professor.nome = data.get("nome", professor.nome)
    professor.idade = data.get("idade", professor.idade)
    professor.disciplina = data.get("disciplina", professor.disciplina)

    db.session.commit()
    return jsonify({"message": "Professor atualizado com sucesso!"}), 200

@professores_bp.route("/professores/<int:professor_id>", methods=["DELETE"])
def deletar_professor(professor_id):    
    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({"error": "Professor não encontrado."}), 404

    db.session.delete(professor)
    db.session.commit()
    return jsonify({"message": "Professor deletado com sucesso!"}), 200