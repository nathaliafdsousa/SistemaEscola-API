from flask import Blueprint, request, jsonify
from Models.Atividade import Atividade, db
import requests

atividade_bp = Blueprint("atividade_bp", __name__)

GERENCIAMENTO_URL = "http://localhost:5000"  # serviço de gerenciamento

@atividade_bp.route("/atividades", methods=["POST"])
def criar_atividade():
    """
Cria uma nova atividade após validar a existência de turma e professor associados
---
tags:
  - Atividades
parameters:
  - in: body
    name: body
    required: true
    schema:
      type: object
      properties:
        nome_atividade:
          type: string
          description: Nome da atividade
        descricao:
          type: string
          description: Descrição da atividade
        peso_porcento:
          type: integer
          description: Peso em porcentagem da atividade
        data_entrega:
          type: string
          format: date
          description: Data de entrega da atividade
        turma_id:
          type: integer
          description: ID da turma associada
        professor_id:
          type: integer
          description: ID do professor associado
responses:
  201:
    description: Atividade criada com sucesso
  400:
    description: Dados inválidos
"""

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
    """
    Listar todas as atividades
    ---

    tags:
        - Atividades
    responses:
        200:
            description: Lista de atividades
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1
                        nome_atividade:
                            type: string
                            example: Atividade 1
                        descricao:
                            type: string
                            example: Descrição da Atividade 1
                        peso_porcento:
                            type: integer
                            example: 30
                        data_entrega:
                            type: string
                            format: date
                            example: 2023-12-31
                        turma_id:
                            type: integer
                            example: 3039
                        professor_id:
                            type: integer
                            example: 4040
        404:
            description: Nenhuma atividade encontrada
    """
    atividades = Atividade.query.all()
    if not atividades:
        return jsonify({"mensagem": "Nenhuma atividade encontrada"}), 404
    return jsonify([atv.to_dict() for atv in atividades]), 200

@atividade_bp.route("/atividades/<int:id>", methods=["GET"])
def obter_atividade(id):
    """
    Obter uma atividade específica através do ID
    ---

    tags:
        - Atividades
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: Atividade encontrada
        404:
            description: Atividade não encontrada
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro": "Atividade não encontrada"}), 404
    return jsonify(atividade.to_dict()),200

@atividade_bp.route("/atividades/<int:id>", methods=["PUT"])
def atualizar_atividade(id):
    """
    Atualizar uma atividade existente através do seu ID
    ---

    tags:
        - Atividades
    
    parameters:
        - name: id
          in: path
          type: integer
          required: true
        - in: body
          name: body
          schema:
            type: object
            properties:
                nome_atividade:
                    type: string
                    descricao: Nome da atividade
                descricao:
                    type: string
                    descricao: Descrição da atividade
                peso_porcento:
                    type: integer
                    descricao: Peso em porcentagem da atividade
                data_entrega:
                    type: date
                    descricao: Data de entrega da atividade
                turma_id:
                    type: integer
                    descricao: ID da turma associada
                professor_id:
                    type: integer
                    descricao: ID do professor associado
    responses:
        200:
            description: Atividade atualizada com sucesso
        400:
            description: Dados inválidos
        404:
            description: Atividade não encontrada
    """
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
    """
    Deletar uma atividade através do seu ID
    ---

    tags:
        - Atividades
    
    parameters:
        - name: id
          in: path
          type: integer
          required: true
    responses:
        200:
            description: Atividade excluída com sucesso
        404:
            description: Atividade não encontrada
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({"erro":"Atividade não encontrada"}), 404
    
    db.session.delete(atividade)
    db.session.commit()

    return jsonify({"mensagem": "Atividade deletada com sucesso"}), 200








