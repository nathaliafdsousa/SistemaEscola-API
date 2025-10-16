from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route("/", methods=["GET"])
def pagina_inicial():
    """
    Status da API
    ---
    tags:
    - Status
    description: Retorna uma mensagem de status para indicar que a API está funcionando.
    produces:
    - application/json
    responses:
        200:
            description: API está operacional
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: Bem vindo à API do Sistema Escolar!
    """
    return jsonify({"message": "Bem vindo à API do Sistema Escolar!"})
