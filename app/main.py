from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_audio, routes_caso

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ou ["*"] para liberar geral (não recomendado em produção)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_audio.router)
app.include_router(routes_caso.router)