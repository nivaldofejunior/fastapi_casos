from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AudioResponse(BaseModel):
    id: UUID
    caminho_arquivo: str
    transcricao: str | None
    data_envio: datetime

    class Config:
        from_attributes = True