from uuid import UUID
from app.database import SessionLocal
from app.models import usuario as models_usuario
from app.models import caso as models_caso
from app.models import audio as models_audio
import os
import uuid
from datetime import datetime
from fastapi import UploadFile
from pathlib import Path

AUDIO_DIR = Path("uploads/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def salvar_arquivo(file: UploadFile) -> str:
    nome_arquivo = f"{uuid.uuid4()}_{normalize_filename(file.filename)}"
    caminho = AUDIO_DIR / nome_arquivo

    with open(caminho, "wb") as buffer:
        buffer.write(file.file.read())

    return str(caminho)

def criar_entrada_completa(cpf_usuario: str, titulo: str, file: UploadFile, db, transcricao: str = None):
    # 1. Verifica ou cria usuário
    usuario = db.query(models_usuario.Usuario).filter_by(cpf=cpf_usuario).first()
    if not usuario:
        usuario = models_usuario.Usuario(cpf=cpf_usuario)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    # 2. Verifica ou cria caso
    caso = (
        db.query(models_caso.Caso)
        .filter_by(usuario_id=usuario.id, titulo=titulo)
        .first()
    )
    if not caso:
        caso = models_caso.Caso(titulo=titulo, usuario_id=usuario.id)
        db.add(caso)
        db.commit()
        db.refresh(caso)

    # 3. Salva o áudio
    caminho = salvar_arquivo(file)

    # 4. Cria entrada do áudio
    audio = models_audio.Audio(
        caso_id=caso.id,
        caminho_arquivo=caminho,
        transcricao=transcricao,
        data_envio=datetime.utcnow(),
    )
    db.add(audio)
    db.commit()
    db.refresh(audio)

    return audio

def criar_entrada_audio_existente(caso, file: UploadFile, db, transcricao: str = None):
    # Salva o áudio
    caminho = salvar_arquivo(file)

    # Cria entrada do áudio
    audio = models_audio.Audio(
        caso_id=caso.id,
        caminho_arquivo=caminho,
        transcricao=transcricao,
        data_envio=datetime.utcnow(),
    )
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio

import unicodedata

def normalize_filename(filename: str) -> str:
    filename = unicodedata.normalize("NFKD", filename).encode("ASCII", "ignore").decode("ASCII")
    return filename.replace(" ", "_").replace("(", "").replace(")", "")
