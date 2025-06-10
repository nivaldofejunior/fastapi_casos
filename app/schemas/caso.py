from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from app.schemas.audio import AudioResponse
from app.schemas.texto import TextoResponse

class StatusCaso(str, Enum):
    pendente = "pendente"
    em_atendimento = "em_atendimento"
    recusado = "recusado"

class CasoBase(BaseModel):
    titulo: str
    descricao: str | None = None

class CasoCreate(CasoBase):
    cpf_usuario: str  # recebido junto do áudio

class CasoResponse(CasoBase):
    id: UUID
    status: StatusCaso

    class Config:
        from_attributes = True

class CasoComAudios(CasoResponse):
    audios: list[AudioResponse] = []
    textos: list[TextoResponse] = []

