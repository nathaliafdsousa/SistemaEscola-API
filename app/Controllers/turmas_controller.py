from flask import request, jsonify
from datetime import datetime
from ..config import db
from app.Models.Turma import Turma
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from app.Models.Professor import Professor # Importe o Professor para checar a FK

turmas_bp = Blueprint("turmas", __name__)

@turmas_bp.route("/turmas", methods=["POST"])
def criar_turma():

    """
    Cria uma nova turma
    ---
    tags:
    - Turmas
    description: Permite criar uma nova turma
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: body
          name: turma
          description: Dados da nova turma que será criada
          required: true
          schema:
            type: object
            required:
                - descricao
                - professor_id
            properties:
                descricao:
                    type: string
                    example: ADS 3AN
                ativo:
                    type: boolean
                    example: true
                professor_id:
                    type: integer
                    example: 10976
    responses:
        200:
            description: Turma criada
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Turma criada com sucesso!
        400:
            description: Erro na criação da turma
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível cadastrar turma. Verifique os dados fornecidos.
    """

    try:
        data = request.get_json()

        descricao = data.get("descricao")
        ativo = data.get("ativo")
        professor_id = data.get("professor_id")
        
        # Opcionalmente, adicione uma verificação para garantir que o professor_id existe
        if professor_id is not None and Professor.query.get(professor_id) is None:
             return jsonify({"error": "Professor ID fornecido não existe."}), 400

        nova_turma = Turma(descricao=descricao, ativo=ativo, professor_id=professor_id)
        db.session.add(nova_turma)
        db.session.commit()

        return jsonify({"message": "Turma criada com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar turma. Verifique os dados fornecidos."}), 400
    except Exception as e:
        # Captura outros erros, incluindo os de validação de dados/tipo
        db.session.rollback()
        return jsonify({"error": f"Erro inesperado ao criar turma: {str(e)}"}), 400
    
@turmas_bp.route("/turmas", methods=["GET"])
def listar_turmas():

    """
    Listar todas as turmas existentes
    ---
    tags:
    - Turmas
    description: Retorna uma lista com todas as turmas cadastradas na base de dados
    produces:
    - application/json
    responses:
        200:
            description: Lista das turmas
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1234
                        descricao:
                            type: string
                            example: ADS
                        ativo:
                            type: boolean
                            example: true
                        professor_id:
                            type: integer
                            example: 10976
        400:
            description: Erro na listagem das turmas
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível listar as turmas.
    """
    try:
        turmas = Turma.query.all()
        resultado = []
        for turma in turmas:
            resultado.append({
                "id": turma.id,
                "descricao": turma.descricao,
                "ativo": turma.ativo,
                "professor_id": turma.professor_id
            })
        return jsonify(resultado), 200
    except Exception:
        return jsonify({"error": "Não foi possível listar as turmas."}), 400

@turmas_bp.route("/turmas/<int:turma_id>", methods=["GET"])
def obter_turma(turma_id):
    
    """
    Fornece as informações de uma turma específica com base em seu ID.
    ---
    tags:
    - Turmas
    description: Retorna os detalhes de uma turma a partir do seu ID
    produces:
    - application/json
    parameters:
        - in: path
          name: turma_id
          type: integer
          required: true
          description: ID identificador da turma que deseja obter informações
    responses:
        200:
            description: Informações da turma especificada
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 1234
                    descricao:
                        type: string
                        example: ADS
                    ativo:
                        type: boolean
                        example: true
                    professor_id:
                        type: integer
                        example: 10976
        404:
            description: Turma não encontrada
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Turma não encontrada.
    """

    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 404

    resultado = {
        "id": turma.id,
        "descricao": turma.descricao,
        "ativo": turma.ativo,
        "professor_id": turma.professor_id
    }
    return jsonify(resultado), 200

@turmas_bp.route("/turmas/<int:turma_id>", methods=["PUT"])
def atualizar_turma(turma_id):
    
    """
    Atualizar informações de uma turma já existente
    ---
    tags:
    - Turmas
    description: Permite atualizar dados de uma turma
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: path
          name: turma_id
          type: integer
          required: true
          description: ID da turma que será atualizada
        - in: body
          name: turma
          description: Dados atualizados da turma
          required: true
          schema:
            type: object
            properties:
                descricao:
                    type: string
                    example: ADS 3BN
                ativo:
                    type: boolean
                    example: true
                professor_id:
                    type: integer
                    example: 10977
    responses:
        200:
            description: Turma atualizada
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Turma atualizada com sucesso!
        404:
            description: Turma não encontrada
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível encontrar a turma para atualizar.
    """

    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 404

    data = request.get_json()
    
    professor_id = data.get("professor_id")
    # Opcionalmente, adicione uma verificação para garantir que o professor_id existe
    if professor_id is not None and Professor.query.get(professor_id) is None:
         return jsonify({"error": "Professor ID fornecido não existe."}), 400

    turma.descricao = data.get("descricao", turma.descricao)
    turma.ativo = data.get("ativo", turma.ativo)
    turma.professor_id = professor_id if professor_id is not None else turma.professor_id

    db.session.commit()
    return jsonify({"message": "Turma atualizada com sucesso!"}), 200

@turmas_bp.route("/turmas/<int:turma_id>", methods=["DELETE"])
def deletar_turma(turma_id):

    """
    Excluir uma turma existente a partir de seu ID
    ---
    tags:
    - Turmas
    description: Permite excluir uma turma a partir do seu ID
    produces:
    - application/json
    parameters:
        - in: path
          name: turma_id
          type: integer
          required: true
          description: ID da turma que será excluída
    responses:
        200:
            description: Turma deletada
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Turma excluída com sucesso!
        404:
            description: Turma não encontrada
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível encontrar a turma para excluir.
    """

    turma = Turma.query.get(turma_id)
    if not turma:
        return jsonify({"error": "Turma não encontrada."}), 404

    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma excluída com sucesso!"}), 200
