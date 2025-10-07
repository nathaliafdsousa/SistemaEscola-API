from flask import request, jsonify
from datetime import datetime
from ..config import db
from app.Models.Aluno import Aluno
from flask import Blueprint
from sqlalchemy.exc import IntegrityError

alunos_bp = Blueprint("alunos", __name__)

@alunos_bp.route("/alunos", methods=["POST"])
def criar_aluno():
    """
    Cria um novo aluno
    
    tags:
    - Alunos
    description: Cria um novo aluno com os dados fornecidos no corpo da requisição.
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: body
          name: aluno
          description: Dados do aluno a ser criado
          required: true
          schema:
            type: object
            required:
                - nome
                - idade
                - turma_id
                - data_nascimento
                - nota_semestre1
                - nota_semestre2
            properties:
                nome:
                    type: string
                    example: Maria Silva
                idade:
                    type: integer
                    example: 20
                turma_id:
                    type: integer
                    example: 1
                data_nascimento:
                    type: string
                    format: date
                    example: 2005-05-15
                nota_semestre1:
                    type: number
                    format: float
                    example: 8.5
                nota_semestre2:
                    type: number
                    format: float
                    example: 5.0
    responses:
        200:
            description: Aluno criado com sucesso
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Aluno criado com sucesso!
        400:
            description: Erro ao criar aluno
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível cadastrar aluno. Verifique os dados fornecidos.
    """

    try:
        data = request.get_json()

        nome = data.get("nome")
        idade = data.get("idade")
        turma_id = data.get("turma_id")
        data_nascimento_str = data.get("data_nascimento")
        nota_semestre1 = data.get("nota_semestre1")
        nota_semestre2 = data.get("nota_semestre2")
        media_final = (nota_semestre1 + nota_semestre2) / 2 if nota_semestre1 is not None and nota_semestre2 is not None else None

        novo_aluno = Aluno(
            nome=nome,
            idade=idade,
            turma_id=turma_id,
            data_nascimento=datetime.strptime(data_nascimento_str, "%Y-%m-%d") if data_nascimento_str else None,
            nota_semestre1=nota_semestre1,
            nota_semestre2=nota_semestre2,
            media_final=media_final
        )
        db.session.add(novo_aluno)
        db.session.commit()

        return jsonify({"message": "Aluno criado com sucesso!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar aluno. Verifique os dados fornecidos."}), 400


@alunos_bp.route("/alunos", methods=["GET"])
def listar_alunos():
    
    """
    Retorna uma lista com todos os alunos existentes.
    
    tags:
    - Alunos
    description: Retorna uma lista com todos os alunos existentes.
    produces:
    - application/json
    responses:
        200:
            description: Lista de alunos
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1
                        nome:
                            type: string
                            example: Maria Silva
                        idade:
                            type: integer
                            example: 20
                        turma_id:
                            type: integer
                            example: 3039
                        data_nascimento:
                            type: string
                            format: date
                            example: 2001-01-11
                        nota_semestre1:
                            type: number
                            format: float
                            example: 8.25
                        nota_semestre2:
                            type: number
                            format: float
                            example: 1.5
                        media_final:
                            type: number
                            format: float
                            example: 4.875
        400:
            description: Erro ao tentar listar alunos
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível listar os alunos
    """
    try:
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
    except Exception:
        return jsonify({"error": "Não foi possível listar os alunos"}), 400


@alunos_bp.route("/alunos/<int:aluno_id>", methods=["GET"])
def obter_aluno(aluno_id):

    """
    Retorna as informações de um aluno específico baseado em seu ID

    tags:
    - Alunos
    description: Retorna as informações de um aluno baseado em seu ID.
    produces:
    - application/json
    parameters:
        - in: path
          name: aluno_id
          description: ID do aluno que será usado para identificá-lo
          required: true
          type: integer
    responses:
        200:
            description: Informações do aluno retornada com sucesso
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 2403658
                    nome:
                        type: string
                        example: Maria Silva
                    idade:
                        type: integer
                        example: 25
                    turma_id:
                        type: integer
                        example: 3039
                    data_nascimento:
                        type: string
                        format: date
                        example: 1998-03-22
                    nota_semestre1:
                        type: number
                        format: float
                        example: 6.75
                    nota_semestre2:
                        type: number
                        format: float
                        example: 4.0
                    media_final:
                        type: number
                        format: float
                        example: 5.375
        404:
            description: Erro ao tentar obter informações do aluno especificado
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Aluno não encontrado. Favor verificar o ID informado.
    """
    
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
    """
    Atualiza as informações de um aluno com base em seu ID.

    tags:
    - Alunos
    description: Atualiza as informações de um aluno com base em seu ID.
    consumes:
    - application/json
    produces:
    - application/json
    parameters:
        - in: path
          name: aluno_id
          description: ID do aluno que terá dados atualizados
          required: true
          type: integer
        - in: body
          name: aluno
          description: Dados do aluno que serão atualizados
          required: true
          schema:
            type: object
            properties:
                nome:
                    type: string
                    example: Maria José
                idade:
                    type: integer
                    example: 21
                turma_id:
                    type: integer
                    example: 3039
                data_nascimento:
                    type: string
                    format: date
                    example: 2002-07-19
                nota_semestre1:
                    type: number
                    format: float
                    example: 7.0
                nota_semestre2:
                    type: number
                    format: float
                    example: 6.5
    responses:
        200:
            description: Aluno atualizado com sucesso
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Aluno atualizado com sucesso!
        400:
            description: Erro ao tentar atualizar o aluno
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Não foi possível atualizar o aluno. Verifique os dados fornecidos.
        404:
            description: Aluno não encontrado para atualização
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Aluno não encontrado
    """
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
    """
    Exclui um aluno da base de dados baseado em seu ID.

    tags:
    - Alunos
    description: Exclui um aluno com base em seu ID.
    produces:
    - application/json
    parameters:
        - in: path
          name: aluno_id
          description: ID do aluno que será excluído da base de dados
          required: true
          type: integer
    responses:
        200:
            description: Aluno deletado com sucesso
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Aluno deletado com sucesso!
        404:
            description: Aluno não encontrado para prosseguir com a exclusão
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Aluno não encontrado      
    """
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"error": "Aluno não encontrado"}), 404
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno deletado com sucesso!"}), 200
