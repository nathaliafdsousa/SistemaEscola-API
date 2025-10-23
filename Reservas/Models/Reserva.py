from sqlalchemy import ForeignKey, Integer, String
import requests
from sqlalchemy.orm import Mapped, mapped_column, relationship #permite definir relacionamentos entre tabelas

id_reserva = db.Column(Integer, primary_key=True)
turma_id = mapped_column(Integer, ForeignKey("turmas.id"), nullable=False)
professor_id = mapped_column(Integer, ForeignKey("professores.id"), nullable = False)
professor_nome = mapped_column(String(100), nullable=False)
materia = mapped_column(String(100), nullable=False)
