from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DATE
from sqlalchemy.orm import Mapped, mapped_column
from config import db

class Nota(db.Model):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nota: Mapped[float] = mapped_column(db.Float, nullable=False)
    aluno_id: Mapped[int] = mapped_column(Integer, nullable=False)
    atividade_id: Mapped[int] = mapped_column(Integer, nullable=False)