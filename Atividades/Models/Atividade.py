from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DATE
from sqlalchemy.orm import Mapped, mapped_column
from config import db

class Atividade(db.Model):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_atividade: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    peso_porcento: Mapped[int] = mapped_column(Integer, nullable=False)
    data_entrega: Mapped[DATE] = mapped_column(DATE, nullable=False)
    turma_id: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_id: Mapped[int] = mapped_column(Integer, nullable=False)

