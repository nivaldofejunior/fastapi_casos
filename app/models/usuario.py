from sqlalchemy import Column, String, Uuid
from app.database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String, unique=True, index=True)
    nome = Column(String, nullable=True)
