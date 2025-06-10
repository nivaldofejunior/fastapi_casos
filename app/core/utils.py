import os
import uuid
from pydub import AudioSegment

def converter_para_wav(caminho_entrada: str, pasta_saida: str) -> str:
    # Garante extensão de entrada correta
    extensao = os.path.splitext(caminho_entrada)[-1].lower()
    
    if extensao not in [".mp3", ".m4a", ".ogg", ".wav", ".opus", ".waptt"]:
        raise ValueError("Formato de áudio não suportado.")

    # Força extensão .opus se for .waptt (comportamento do WhatsApp)
    if extensao == ".waptt":
        temp_opus = caminho_entrada + ".opus"
        os.rename(caminho_entrada, temp_opus)
        caminho_entrada = temp_opus

    # Gera nome de saída
    nome_saida = f"{uuid.uuid4()}.wav"
    caminho_saida = os.path.join(pasta_saida, nome_saida)

    # Converte para wav com pydub
    audio = AudioSegment.from_file(caminho_entrada)
    audio.export(caminho_saida, format="wav")

    return caminho_saida
