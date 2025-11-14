from flask import Blueprint, request, jsonify
from Models.Nota import Nota, db
import requests

notatividade_bp = Blueprint("notatividade_bp", __name__)

GERENCIAMENTO_URL = "http://localhost:5000"

@notatividade_bp.route("/notas", methods=["POST"])
def criar_nota():
    """
    Criar uma nova nota
    ---
    tags:
      - Notas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nota:
              type: number
              format: float
            aluno_id:
              type: integer
            atividade_id:
              type: integer
    responses:
      201:
        description: Nota criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nota:
              type: number
              format: float
              example: 8.5
            aluno_id:
              type: integer
              example: 3039
            atividade_id:
              type: integer
              example: 4040
      400:
        description: Dados inválidos
    """
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
    """
    Listar todas as notas
    ---
    tags:
      - Notas
    responses:
      200:
        description: Lista de notas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nota:
                type: number
                format: float
                example: 8.5
              aluno_id:
                type: integer
                example: 3039
              atividade_id:
                type: integer
                example: 4040
      404:
        description: Nenhuma nota encontrada
    """
    notas = Nota.query.all()

    if not notas:
        return jsonify({"erro":"Nenhuma nota encontrada"}), 404
    return jsonify([nt.to_dict() for nt in notas]), 200


@notatividade_bp.route("/notas/<int:id>", methods=["GET"])
def obter_nota(id):
    """
    Obter uma nota específica através do seu ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Nota encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nota:
              type: number
              format: float
              example: 8.5
            aluno_id:
              type: integer
              example: 3039
            atividade_id:
              type: integer
              example: 4040
      404:
        description: Nota não encontrada
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro":"Nota não encontrada"}), 404
    return jsonify(nota.to_dict()),200


@notatividade_bp.route("/notas/<int:id>", methods=["PUT"])
def atualizar_nota(id):
    """
    Atualizar uma nota existente através do ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nota:
              type: number
              format: float
            aluno_id:
              type: integer
            atividade_id:
              type: integer
    responses:
      200:
        description: Nota atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nota:
              type: number
              format: float
              example: 9.0
            aluno_id:
              type: integer
              example: 3039
            atividade_id:
              type: integer
              example: 4040
      400:
        description: Dados inválidos
      404:
        description: Nota não encontrada
    """
    data = request.json
    nota = Nota.query.get(id)

    if not nota:
        return jsonify({"erro":"Nota não encontrada"}), 404
    
    if "aluno_id" in data:
        r_aluno = requests.get(f"{GERENCIAMENTO_URL}/alunos/{data['aluno_id']}")
        if r_aluno.status_code != 200:
            return jsonify({"erro":"Aluno não encontrado"}), 400
        nota.aluno_id = data["aluno_id"]
    
    if "atividade_id" in data:
        r_atividade = requests.get(f"{GERENCIAMENTO_URL}/atividades/{data['atividade_id']}")
        if r_atividade.status_code != 200:
            return jsonify({"erro":"Atividade não encontrada"}), 400
        nota.atividade_id = data["atividade_id"]

    nota.nota = data.get("nota", nota.nota)
    db.session.commit()

    return jsonify({"message":"Nota atualizada com sucesso"}), 200


@notatividade_bp.route("/notas/<int:id>", methods=["DELETE"])
def deletar_nota(id):
    """
    Deletar uma nota através do ID
    ---
    tags:
      - Notas
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Nota excluída com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Nota excluída com sucesso
      404:
        description: Nota não encontrada para exclusão
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({"erro":"Nota não encontrada"}), 404
    
    db.session.delete(nota)
    db.session.commit()

    return jsonify({"message":"Nota deletada com sucesso"}), 200
