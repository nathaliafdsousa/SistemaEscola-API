from flask import request, jsonify
from datetime import datetime
from Models import db, Professor  
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
professores_bp = Blueprint("professores", __name__)

@professores_bp.route("/professores", methods=["POST"])
def criar_professor():
    
    """
    Cria um novo professor

    tags:
    - professores
    description: Permite a criação de um novo professor
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: body
        name: professor
        description: Dados do professor que será criado
        required: true
        schema:
            type: object
            properties:
                nome:
                    type: string
                    example: Jorge Fernandes
                idade:
                    type: integer
                    example: 40
                disciplina:
                    type: string
                    example: Matemática
    responses:
        200:
            description: Professor criado
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Professor criado com sucesso!
        400:
            description: Erro na criação do professor
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível cadastrar professor. Verifique os dados fornecidos.
    """
    try:
        data = request.get_json()

        nome = data.get("nome")
        idade = data.get("idade")
        disciplina = data.get("disciplina")

        novo_professor = Professor(nome=nome, idade=idade, disciplina=disciplina)
        db.session.add(novo_professor)
        db.session.commit()

        return jsonify({"message": "Professor criado com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar professor. Verifique os dados fornecidos."}), 400
    
@professores_bp.route("/professores", methods=["GET"])
def listar_professores():

    """
    Lista todos os professores existentes na base de dados.

    tags:
    - professores
    description: Retorna uma lista de todos os professores cadastrados
    produces:
    - application/json
    responses:
        200:
            description: Lista de professores
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1322
                        nome:
                            type: string
                            example: Jorge Fernandes
                        idade:
                            type: integer
                            example: 40
                        disciplina:
                            type: string
                            example: Matemática
        400:
            description: Erro ao tentar listar os professores
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível listar os professores.
    """

    try:
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
    except Exception:
        return jsonify({"error": "Não foi possível listar os professores."}), 400

@professores_bp.route("/professores/<int:professor_id>", methods=["GET"])
def obter_professor(professor_id):
    
    """
    Retornar as informações de um professor a partir de seu ID.

    tags:
    - professores
    description: Retorna os detalhes de um professor específico através do seu ID
    produces:
    - application/json
    parameters:
        - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor que deseja obter informações
    responses:
        200:
            description: Informações do professor especificado
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 1322
                    nome:
                        type: string
                        example: Jorge Fernandes
                    idade:
                        type: integer
                        example: 40
                    disciplina:
                        type: string
                        example: Matemática
        404:
            description: Professor não encontrado
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Professor não encontrado.
    """

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

    """
    Atualiza as informações de um professor a partir do seu ID.

    tags:
    - professores
    description: Permite atualizar os detalhes de um professor a partir de seu ID.
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor que será atualizado
         - in: body
        name: professor
        description: Dados atualizados do professor
        required: true
        schema:
            type: object
            properties:
                nome:
                    type: string
                    example: Jorge Felippo
                idade:
                    type: integer
                    example: 40
                disciplina:
                    type: string
                    example: Matemática
    responses:
        200:
            description: Professor atualizado
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Professor atualizado com sucesso!
        404:
            description: Professor não encontrado
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Professor não encontrado.                
    """

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
    
    """
    Exclui um professor a partir de seu ID.

    tags:
    - professores
    description: Possibilita a exclusão de um professor específico através do seu ID
    produces:
    - application/json
    parameters:
        - in: path
        name: professor_id
        type: integer
        required: true
        description: ID do professor que será excluído
    responses:
        200:
            description: Professor deletado
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Professor deletado com sucesso!
        404:
            description: Professor não encontrado
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Professor não encontrado.
    """

    professor = Professor.query.get(professor_id)
    if not professor:
        return jsonify({"error": "Professor não encontrado."}), 404

    db.session.delete(professor)
    db.session.commit()
    return jsonify({"message": "Professor deletado com sucesso!"}), 200