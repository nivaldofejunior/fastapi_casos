from fastapi import APIRouter, UploadFile, Form, Depends, File, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.audio_service import criar_entrada_completa, criar_entrada_audio_existente
from app.schemas.audio import AudioResponse
from pydub import AudioSegment
import requests
import os
import tempfile

router = APIRouter(prefix="/audios", tags=["Audios"])

GROQ_API_KEY = "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"
GROQ_WHISPER_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/audio/upload", response_model=AudioResponse)
async def upload_audio(
    file: UploadFile = File(...),
    caso_id: str = Form(...),
    db: Session = Depends(get_db)
):
    # Buscar o caso pelo ID
    from app.models.caso import Caso as models_caso
    caso = db.query(models_caso).filter_by(id=caso_id).first()
    if not caso:
        raise HTTPException(status_code=404, detail="Caso não encontrado.")

    # Salva o arquivo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_audio:
        temp_audio.write(await file.read())
        temp_audio_path = temp_audio.name

    # Converte para WAV
    wav_path = temp_audio_path + ".wav"
    try:
        audio = AudioSegment.from_file(temp_audio_path)
        audio.export(wav_path, format="wav")
    except Exception as e:
        os.remove(temp_audio_path)
        raise HTTPException(status_code=400, detail=f"Erro ao converter para WAV: {e}")

    # Envia para o Whisper da Groq
    with open(wav_path, "rb") as wav_file:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        files = {
            "file": ("audio.wav", wav_file, "audio/wav")
        }
        data = {
            "model": "whisper-large-v3"
        }
        response = requests.post(GROQ_WHISPER_URL, headers=headers, files=files, data=data)

    os.remove(temp_audio_path)
    os.remove(wav_path)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na transcrição com Whisper")
    transcricao = response.json().get("text", "")

    # Recria UploadFile para salvar o arquivo original
    file.file.seek(0)
    audio_obj = criar_entrada_audio_existente(
        caso=caso,
        file=file,
        db=db,
        transcricao=transcricao
    )
    return audio_obj
