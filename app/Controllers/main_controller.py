from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def pagina_inicial():
    """
    Pagina inicial para mostrar que a API está funcionando.
    """
    return jsonify({"message":"Bem vindo à API do Sistema Escolar!"})