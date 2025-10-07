from . import create_app
from flask import Flask, jsonify

app = create_app()

from app.Controllers.alunos_controller import alunos_bp
from app.Controllers.professor_controller import professores_bp
from app.Controllers.turmas_controller import turmas_bp

app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(turmas_bp)

@app.route("/health")
def home():
    return jsonify({"message":"API Sistema Escolar rodando no container!"})

if __name__ == "__main__":
    app.run(debug=True) #debug=True ativa o modo debug e reinicia o servidor automaticamente ao detectar mudanças no código