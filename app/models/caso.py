from sqlalchemy import Column, String, Enum, ForeignKey, Uuid
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
import enum

class StatusCaso(str, enum.Enum):
    pendente = "pendente"
    em_atendimento = "em_atendimento"
    recusado = "recusado"

class Caso(Base):
    __tablename__ = "casos"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(Uuid(as_uuid=True), ForeignKey("usuarios.id"))
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    status = Column(Enum(StatusCaso), default=StatusCaso.pendente)

    audios = relationship("Audio", back_populates="caso")
    textos = relationship("Texto", back_populates="caso")
