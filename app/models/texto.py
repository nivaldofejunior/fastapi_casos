from sqlalchemy import Column, String, ForeignKey, Uuid, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Texto(Base):
    __tablename__ = "textos"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caso_id = Column(Uuid(as_uuid=True), ForeignKey("casos.id"))
    conteudo = Column(Text, nullable=False)
    data_envio = Column(DateTime, default=datetime.utcnow)

    caso = relationship("Caso", back_populates="textos") 