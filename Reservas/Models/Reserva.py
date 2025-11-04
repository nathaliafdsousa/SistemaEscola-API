from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from config import db


class Reserva(db.Model):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    turma_id: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_id: Mapped[int] = mapped_column(Integer, nullable=False)
    professor_nome: Mapped[str] = mapped_column(String(100), nullable=False)
    materia: Mapped[str] = mapped_column(String(100), nullable=False)
    data_reserva: Mapped[str] = mapped_column(String(10), nullable=False)  

