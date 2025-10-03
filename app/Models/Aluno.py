from app import db
from sqlalchemy import ForeignKey

class Aluno (db.Model):
    __tablename__ = "alunos"
   
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    idade = db.Column(db.Integer, nullable = False)
    turma_id = db.Column(db.Integer, ForeignKey("turmas.id"),nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_semestre1 = db.Column(db.Float, nullable=False)
    nota_semestre2 = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Aluno {self.nome}>"