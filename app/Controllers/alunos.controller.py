from flask import request, jsonify
from datetime import datetime
from Models import db, Aluno  
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
alunos_bp = Blueprint("alunos", __name__)

@alunos_bp.route("/alunos", methods=["POST"])
def criar_aluno():
    try:
        data = request.get_json()

        nome = data.get("nome")
        idade = data.get("idade")
        turma_id = data.get("turma_id")
        data_nascimento_str = data.get("data_nascimento")
        nota_semestre1 = data.get("nota_semestre1")
        nota_semestre2 = data.get("nota_semestre2")
        media_final = (nota_semestre1 + nota_semestre2) / 2  if nota_semestre1 is not None and nota_semestre2 is not None else None
        db.session.add(criar_aluno)
        db.session.commit()

        return jsonify({"message": "Aluno criado com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar aluno. Verifique os dados fornecidos."}), 400
    

@alunos_bp.route("/alunos", methods=["GET"])
def listar_alunos():
    alunos = Aluno.query.all()
    resultado = []
    for aluno in alunos:
        resultado.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "idade": aluno.idade,
            "turma_id": aluno.turma_id,
            "data_nascimento": aluno.data_nascimento.strftime("%Y-%m-%d"),
            "nota_semestre1": aluno.nota_semestre1,
            "nota_semestre2": aluno.nota_semestre2,
            "media_final": aluno.media_final
        })
    return jsonify(resultado), 200

@alunos_bp.route("/alunos/<int:aluno_id>", methods=["GET"])
def obter_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    resultado = {
        "id": aluno.id,
        "nome": aluno.nome,
        "idade": aluno.idade,       
        "turma_id": aluno.turma_id,
        "data_nascimento": aluno.data_nascimento.strftime("%Y-%m-%d"),
        "nota_semestre1": aluno.nota_semestre1,
        "nota_semestre2": aluno.nota_semestre2,
        "media_final": aluno.media_final
    }
    return jsonify(resultado), 200

@alunos_bp.route("/alunos/<int:aluno_id>", methods=["PUT"])
def atualizar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    try:
        data = request.get_json()

        aluno.nome = data.get("nome", aluno.nome)
        aluno.idade = data.get("idade", aluno.idade)
        aluno.turma_id = data.get("turma_id", aluno.turma_id)
        
        data_nascimento_str = data.get("data_nascimento")
        if data_nascimento_str:
            aluno.data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
        
        aluno.nota_semestre1 = data.get("nota_semestre1", aluno.nota_semestre1)
        aluno.nota_semestre2 = data.get("nota_semestre2", aluno.nota_semestre2)
        if aluno.nota_semestre1 is not None and aluno.nota_semestre2 is not None:
            aluno.media_final = (aluno.nota_semestre1 + aluno.nota_semestre2) / 2

        db.session.commit()
        return jsonify({"message": "Aluno atualizado com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível atualizar o aluno. Verifique os dados fornecidos."}), 400
    
@alunos_bp.route("/alunos/<int:aluno_id>", methods=["DELETE"])
def deletar_aluno(aluno_id):
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso!"}), 200 

    

    

        




