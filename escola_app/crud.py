from sqlalchemy.orm import Session

from . import models, schemas


def get_aluno(db: Session, id_aluno: int):
    return db.query(models.Aluno).filter(models.Aluno.id_aluno == id_aluno).first()


def get_aluno_by_nome(db: Session, nome: str):
    return db.query(models.Aluno).filter(models.Aluno.nome == nome).first()


def get_alunos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aluno).offset(skip).limit(limit).all()


def create_aluno(db: Session, aluno: schemas.Aluno):
    db_aluno = models.Aluno(nome=aluno.nome,
                            nome_professor = aluno.nome_professor,
                            idade = aluno.idade,
                            nota_primeiro_semestre = aluno.nota_primeiro_semestre,
                            nota_segundo_semestre = aluno.nota_segundo_semestre,
                            numero_sala = aluno.numero_sala
                            )

    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

def delete_aluno(db: Session, id_aluno: int):
    aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == id_aluno).first()
    if aluno:
        db.delete(aluno)
        db.commit()
        return True  # Retorna True para indicar que o aluno foi excluído com sucesso
    else:
        return False  # Retorna False para indicar que o aluno não foi encontra
    
def update_aluno(db: Session, id_aluno: int, aluno_update: schemas.Aluno):
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id_aluno == id_aluno).first()
    
    if db_aluno is None:
        return False  # Return False to indicate that the aluno was not found
    db_aluno.nome_professor = aluno_update.nome_professor
    db_aluno.idade = aluno_update.idade
    db_aluno.nota_primeiro_semestre = aluno_update.nota_primeiro_semestre
    db_aluno.nota_segundo_semestre = aluno_update.nota_segundo_semestre
    db_aluno.numero_sala = aluno_update.numero_sala
    
    db.commit()
    
    return True  # Return True to indicate a successful update
