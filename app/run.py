from . import create_app
from flask import Flask, jsonify

app = create_app()

@app.route("/health")
def home():
    return jsonify({"message":"API Sistema Escolar rodando no container!"})

if __name__ == "__main__":
    app.run(debug=True) #debug=True ativa o modo debug e reinicia o servidor automaticamente ao detectar mudanças no código