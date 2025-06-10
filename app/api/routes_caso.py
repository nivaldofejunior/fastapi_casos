from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.caso import CasoComAudios
from app.crud import caso as crud_caso
from app.schemas.texto import TextoResponse
from app.models.texto import Texto
from app.models.caso import Caso as models_caso

router = APIRouter(prefix="/casos", tags=["Casos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pendentes", response_model=list[CasoComAudios])
def listar_casos_pendentes(db: Session = Depends(get_db)):
    casos = crud_caso.get_casos_pendentes(db)
    return casos

@router.get("/{cpf}", response_model=list[CasoComAudios])
def listar_casos_por_cpf(cpf: str, db: Session = Depends(get_db)):
    casos = crud_caso.get_casos_por_cpf(db, cpf)
    if not casos:
        raise HTTPException(status_code=404, detail="Nenhum caso encontrado para esse CPF.")
    return casos

from fastapi import status

@router.post("/{id}/aceitar", response_model=CasoComAudios, status_code=status.HTTP_200_OK)
def aceitar_caso(id: str, db: Session = Depends(get_db)):
    caso = crud_caso.aceitar_caso(db, id)
    if not caso:
        raise HTTPException(status_code=404, detail="Caso não encontrado.")
    return caso

@router.get("/aceitos", response_model=list[CasoComAudios])
def listar_casos_aceitos(db: Session = Depends(get_db)):
    casos = crud_caso.get_casos_aceitos(db)
    return casos

@router.post("/{id}/texto", response_model=TextoResponse)
def adicionar_texto_ao_caso(id: str, conteudo: str = Form(...), db: Session = Depends(get_db)):
    caso = db.query(models_caso).filter_by(id=id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso não encontrado.")
    texto = Texto(caso_id=caso.id, conteudo=conteudo)
    db.add(texto)
    db.commit()
    db.refresh(texto)
    return texto

@router.post("/", response_model=CasoComAudios)
def criar_caso(
    cpf_usuario: str = Form(...),
    titulo: str = Form(...),
    descricao: str = Form(None),
    db: Session = Depends(get_db)
):
    from app.models import usuario as models_usuario
    from app.models.caso import Caso as models_caso
    usuario = db.query(models_usuario.Usuario).filter_by(cpf=cpf_usuario).first()
    if not usuario:
        usuario = models_usuario.Usuario(cpf=cpf_usuario)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
    caso = db.query(models_caso).filter_by(usuario_id=usuario.id, titulo=titulo).first()
    if caso:
        raise HTTPException(status_code=400, detail="Já existe um caso com esse título para esse usuário.")
    caso = models_caso(titulo=titulo, descricao=descricao, usuario_id=usuario.id)
    db.add(caso)
    db.commit()
    db.refresh(caso)
    return caso

@router.get("/buscar_por_titulo", response_model=CasoComAudios)
def buscar_caso_por_titulo(
    cpf_usuario: str,
    titulo: str,
    db: Session = Depends(get_db)
):
    from app.models import usuario as models_usuario
    from app.models.caso import Caso as models_caso
    usuario = db.query(models_usuario.Usuario).filter_by(cpf=cpf_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    caso = db.query(models_caso).filter_by(usuario_id=usuario.id, titulo=titulo).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso não encontrado para esse título e CPF.")
    return caso

@router.get("/", response_model=list[CasoComAudios])
def listar_todos_casos(db: Session = Depends(get_db)):
    from app.models.caso import Caso as models_caso
    casos = db.query(models_caso).all()
    return casos
