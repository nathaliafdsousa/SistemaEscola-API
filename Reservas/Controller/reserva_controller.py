from flask import Blueprint, request, jsonify
from Models.Reserva import Reserva, db
import requests

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.get_json()
    turma_id = data.get('turma_id')
    professor_id = data.get('professor_id')








