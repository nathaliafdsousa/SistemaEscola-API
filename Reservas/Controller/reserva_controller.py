from flask import Blueprint, request, jsonify
from Models.Reserva import Reserva, db
import requests

reserva_bp = Blueprint('reserva_bp', __name__)

GERENCIAMENTO_URL = "http://localhost:5000"  # serviço de gerenciamento


@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    """
    Criar uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            turma_id:
              type: integer
            professor_id:
              type: integer
            professor_nome:
              type: string
            materia:
              type: string
            data_reserva:
              type: string
    responses:
      201:
        description: Reserva criada com sucesso
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

    reserva = Reserva(**data)
    db.session.add(reserva)
    db.session.commit()

    return jsonify(reserva.to_dict()), 201


@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    """
    Listar todas as reservas
    ---
    tags:
      - Reservas
    responses:
      200:
        description: Lista de reservas
    """
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas]), 200


@reserva_bp.route('/reservas/<int:id>', methods=['GET'])
def buscar_reserva(id):
    """
    Buscar reserva por ID
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Reserva encontrada
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404
    return jsonify(reserva.to_dict()), 200


@reserva_bp.route('/reservas/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    """
    Atualizar uma reserva
    ---
    tags:
      - Reservas
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
            turma_id:
              type: integer
            professor_id:
              type: integer
            professor_nome:
              type: string
            materia:
              type: string
            data_reserva:
              type: string
    responses:
      200:
        description: Reserva atualizada
      404:
        description: Reserva não encontrada
    """
    data = request.json
    reserva = Reserva.query.get(id)

    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    if 'turma_id' in data:
        r_turma = requests.get(f"{GERENCIAMENTO_URL}/turmas/{data['turma_id']}")
        if r_turma.status_code != 200:
            return jsonify({"erro": "Turma inválida"}), 400
        reserva.turma_id = data['turma_id']

    if 'professor_id' in data:
        r_prof = requests.get(f"{GERENCIAMENTO_URL}/professores/{data['professor_id']}")
        if r_prof.status_code != 200:
            return jsonify({"erro": "Professor inválido"}), 400
        reserva.professor_id = data['professor_id']

    reserva.professor_nome = data.get('professor_nome', reserva.professor_nome)
    reserva.materia = data.get('materia', reserva.materia)
    reserva.data_reserva = data.get('data_reserva', reserva.data_reserva)

    db.session.commit()
    return jsonify(reserva.to_dict()), 200


@reserva_bp.route('/reservas/<int:id>', methods=['DELETE'])
def deletar_reserva(id):
    """
    Deletar uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Reserva deletada com sucesso
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"mensagem": "Reserva deletada com sucesso"}), 200







