from app import db

class Turma(db.Model):
    __tablename__ ="turmas"

    id = db.Column(Integer, primary_key = True)
    descricao = db.Column(String(100), nullable=False)
    professor_id = db.Column(Integer, ForeignKey("professor.id"), nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)