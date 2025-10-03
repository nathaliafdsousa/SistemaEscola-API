from app import db
from sqlalchemy import ForeignKey, Integer, String, Boolean

class Turma(db.Model):
    __tablename__ ="turmas"

    id = db.Column(Integer, primary_key = True)
    descricao = db.Column(String(100), nullable=False)
    professor_id = db.Column(Integer, ForeignKey("professores.id"), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Turma {self.descricao}>"