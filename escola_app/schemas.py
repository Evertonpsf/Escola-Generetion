from pydantic import BaseModel




class Aluno(BaseModel):
    id_aluno: int
    nome: str
    nome_professor: str
    idade: int
    nota_primeiro_semestre: float
    nota_segundo_semestre: float 
    numero_sala: str
    class Config:
        orm_mode = True