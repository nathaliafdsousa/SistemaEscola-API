from app import db

class Professor (db.Model):
    __tablename__ = "professores"
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    materia = db.Column(db.String(100), nullable = False)
    observacoes = db.Column(db.String(120), nullable = False)