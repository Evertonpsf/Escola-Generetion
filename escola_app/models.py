from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, FLOAT
from sqlalchemy.orm import relationship

from .database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id_aluno = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    nome_professor = Column(String, unique=False, index=True) 
    idade = Column(Integer, unique=False, index=True)
    nota_primeiro_semestre = Column(FLOAT, unique=False, index=True)
    nota_segundo_semestre = Column(FLOAT, unique=False, index=True)
    numero_sala = Column(String, unique=False, index=True)

