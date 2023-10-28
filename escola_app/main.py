from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request):
    return request.state.db


@app.post("/alunos/", response_model=schemas.Aluno)
def create_aluno(aluno: schemas.Aluno, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno_by_nome(db, nome=aluno.nome)
    if db_aluno:
        raise HTTPException(status_code=400, detail="Aluno ja matriculado")
    return crud.create_aluno(db=db, aluno=aluno)


@app.get("/alunos/", response_model=list[schemas.Aluno])
def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alunos = crud.get_alunos(db, skip=skip, limit=limit)
    return alunos


@app.get("/alunos/{id_aluno}", response_model=schemas.Aluno)
def read_aluno(id_aluno: int, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno(db, id_aluno=id_aluno)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return db_aluno



@app.delete("/alunos/{id_aluno}",status_code=204)
def delete_aluno(id_aluno: int, db: Session = Depends(get_db)):
    result = crud.delete_aluno(db, id_aluno=id_aluno)
    if not result:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return "Aluno expulso com sucesso"  # Return a success message

@app.put("/alunos/{id_aluno}", response_model=schemas.Aluno)
def update_aluno(
    id_aluno: int,
    aluno_update: schemas.Aluno,
    db: Session = Depends(get_db)
):
    updated_aluno = crud.update_aluno(db, id_aluno, aluno_update)
    if not updated_aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    db_aluno = crud.get_aluno(db, id_aluno=id_aluno)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno nao encontrado")
    return db_aluno