from sqlalchemy import Column, String, ForeignKey, Uuid, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Audio(Base):
    __tablename__ = "audios"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caso_id = Column(Uuid(as_uuid=True), ForeignKey("casos.id"))
    caminho_arquivo = Column(String, nullable=False)
    transcricao = Column(Text, nullable=True)
    data_envio = Column(DateTime, default=datetime.utcnow)

    caso = relationship("Caso", back_populates="audios")
