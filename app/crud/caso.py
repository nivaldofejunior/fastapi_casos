from sqlalchemy.orm import Session
from app.models import usuario as models_usuario
from app.models import caso as models_caso
from app.models.caso import StatusCaso


def get_casos_pendentes(db: Session):
    from app.models.caso import StatusCaso
    return db.query(models_caso.Caso).filter_by(status=StatusCaso.pendente).all()


def get_casos_por_cpf(db: Session, cpf: str):
    usuario = db.query(models_usuario.Usuario).filter_by(cpf=cpf).first()
    if not usuario:
        return []

    return db.query(models_caso.Caso).filter_by(usuario_id=usuario.id).all()


def aceitar_caso(db: Session, caso_id: str):
    caso = db.query(models_caso.Caso).filter_by(id=caso_id).first()
    if not caso:
        return None
    caso.status = StatusCaso.em_atendimento
    db.commit()
    db.refresh(caso)
    return caso


def get_casos_aceitos(db: Session):
    from app.models.caso import StatusCaso
    return db.query(models_caso.Caso).filter_by(status=StatusCaso.em_atendimento).all()
