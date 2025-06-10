from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TextoResponse(BaseModel):
    id: UUID
    conteudo: str
    data_envio: datetime

    class Config:
        from_attributes = True 