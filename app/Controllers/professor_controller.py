from flask import request, jsonify, Blueprint
from ..config import db
from app.Models.Professor import Professor
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest # Importado para capturar o erro de sintaxe JSON

professores_bp = Blueprint("professores", __name__)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
@professores_bp.route("/professores", methods=["POST"])
def criar_professor():
    """
    Cria um novo professor
    ---
    tags:
    - Professores
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
            required:
                - nome
                - idade
                - materia
            properties:
                nome:
                    type: string
                    example: Jorge Fernandes
                idade:
                    type: integer
                    example: 40
                materia:
                    type: string
                    example: Matemática
                observacoes:
                    type: string
                    example: Professor de 3 turmas
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

        # 1. Checa se o JSON está presente
        if not data:
             return jsonify({"error": "Dados JSON ausentes ou mal formatados."}), 400

        nome = data.get("nome")
        idade = data.get("idade")
        materia = data.get("materia")
        observacoes = data.get("observacoes")

        # 2. Validação básica de campos obrigatórios
        if not nome or idade is None or not materia:
             return jsonify({"error": "Campos 'nome', 'idade' e 'materia' são obrigatórios."}), 400
        
        # Tenta converter idade para int
        try:
             idade = int(idade)
        except ValueError:
             return jsonify({"error": "O campo 'idade' deve ser um número inteiro."}), 400


        novo_professor = Professor(nome=nome, idade=idade, materia=materia, observacoes=observacoes)
        db.session.add(novo_professor)
        db.session.commit()

        return jsonify({"message": "Professor criado com sucesso!"}), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Não foi possível cadastrar professor. Verifique os dados fornecidos (ex: duplicidade)."}), 400
    
    except BadRequest as e:
        # Captura o erro de sintaxe do JSON antes da aplicação tentar processar
        print(f"Erro de decodificação de JSON: {e}")
        return jsonify({"error": f"Erro de sintaxe no JSON: {e.description}"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar professor: {e}")
        return jsonify({"error": "Erro interno do servidor."}), 500


# ----------------------------------------------------------------------
# ROTA: GET /professores (Listagem)
# ----------------------------------------------------------------------
@professores_bp.route("/professores", methods=["GET"])
def listar_professores():
    """
    Lista todos os professores existentes na base de dados.
    ---
    tags:
    - Professores
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
                            example: 1
                        nome:
                            type: string
                            example: Jorge Fernandes
                        idade:
                            type: integer
                            example: 40
                        materia:
                            type: string
                            example: Matemática
                        observacoes:
                            type: string
                            example: Professor de 3 turmas
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
                "materia": professor.materia,
                "observacoes": professor.observacoes if hasattr(professor, 'observacoes') else None # Garante que observacoes é incluído
            })
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro ao listar professores: {e}")
        return jsonify({"error": "Não foi possível listar os professores."}), 500


# ----------------------------------------------------------------------
# ROTA: GET /professores/<int:professor_id> (Busca por ID)
# ----------------------------------------------------------------------
@professores_bp.route("/professores/<int:professor_id>", methods=["GET"])
def obter_professor(professor_id):
    
    """
    Retornar as informações de um professor a partir de seu ID.
    ---
    tags:
    - Professores
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
                        example: 1
                    nome:
                        type: string
                        example: Jorge Fernandes
                    idade:
                        type: integer
                        example: 40
                    materia:
                        type: string
                        example: Matemática
                    observacoes:
                        type: string
                        example: Professor de 3 turmas
        404:
            description: Professor não encontrado
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example: Professor não encontrado.
    """
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado."}), 404

        resultado = {
            "id": professor.id,
            "nome": professor.nome,
            "idade": professor.idade,
            "materia": professor.materia,
            "observacoes": professor.observacoes
        }
        return jsonify(resultado), 200
    except Exception as e:
        print(f"Erro ao obter professor por ID: {e}")
        return jsonify({"error": "Erro interno do servidor."}), 500


# ----------------------------------------------------------------------
# ROTA: PUT /professores/<int:professor_id> (Atualização)
# Adicionado tratamento para JSON ausente, erro de sintaxe JSON (BadRequest) 
# e erro de conversão de tipo (ValueError).
# ----------------------------------------------------------------------
@professores_bp.route("/professores/<int:professor_id>", methods=["PUT"])
def atualizar_professor(professor_id):

    """
    Atualiza as informações de um professor a partir do seu ID.
    ---
    tags:
    - Professores
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
                materia:
                    type: string
                    example: Matemática
                observacoes:
                    type: string
                    example: Professor de 1 turma
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
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado."}), 404

        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados JSON ausentes. Certifique-se de usar o header 'Content-Type: application/json'."}), 400

        # Atualização segura dos campos
        if "nome" in data:
            professor.nome = data["nome"]
            
        if "idade" in data:
            try:
                # Tenta garantir que o dado é um inteiro
                professor.idade = int(data["idade"])
            except (TypeError, ValueError):
                return jsonify({"error": "O campo 'idade' deve ser um número inteiro válido."}), 400

        if "materia" in data:
            professor.materia = data["materia"]
            
        if "observacoes" in data:
            professor.observacoes = data["observacoes"]

        db.session.commit()
        return jsonify({"message": "Professor atualizado com sucesso!"}), 200

    except BadRequest as e:
        # Captura o erro de sintaxe do JSON (o que estava te dando dor de cabeça)
        print(f"Erro de decodificação de JSON: {e}")
        return jsonify({"error": f"Erro de sintaxe no JSON: {e.description}"}), 400
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro (PUT /professores/{professor_id}) ao atualizar professor: {e}")
        return jsonify({"error": "Erro interno do servidor."}), 500


# ----------------------------------------------------------------------
# ROTA: DELETE /professores/<int:professor_id> (Exclusão)
# Adicionado tratamento de erro interno.
# ----------------------------------------------------------------------
@professores_bp.route("/professores/<int:professor_id>", methods=["DELETE"])
def deletar_professor(professor_id):
    
    """
    Exclui um professor a partir de seu ID.
    ---
    tags:
    - Professores
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
    try:
        professor = Professor.query.get(professor_id)
        if not professor:
            return jsonify({"error": "Professor não encontrado."}), 404

        db.session.delete(professor)
        db.session.commit()
        return jsonify({"message": "Professor deletado com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao deletar professor: {e}")
        return jsonify({"error": "Erro interno do servidor ao tentar deletar o professor."}), 500



