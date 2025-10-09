from . import create_app
from flask import Flask, jsonify
from .config import db

app = create_app()

with app.app_context():
    db.create_all()

@app.route("/health")
def home():
    return jsonify({"message":"API Sistema Escolar rodando no container!"})

if __name__ == "__main__":
    app.run(debug=True)
