from pydantic import BaseModel, constr
from uuid import UUID

class UsuarioBase(BaseModel):
    cpf: constr(min_length=11, max_length=14)  # pode ser formatado ou só números

class UsuarioCreate(UsuarioBase):
    nome: str | None = None

class UsuarioResponse(UsuarioBase):
    id: UUID
    nome: str | None = None

    class Config:
        from_attributes = True
